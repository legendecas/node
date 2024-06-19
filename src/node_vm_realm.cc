#include "node_vm_realm.h"
#include "node_contextify.h"
#include "node_errors.h"
#include "util-inl.h"

namespace node {

using contextify::ContextifyScript;
using errors::TryCatchScope;
using v8::Context;
using v8::EscapableHandleScope;
using v8::FixedArray;
using v8::Function;
using v8::FunctionTemplate;
using v8::HandleScope;
using v8::Isolate;
using v8::Local;
using v8::MaybeLocal;
using v8::Object;
using v8::ObjectTemplate;
using v8::Promise;
using v8::Script;
using v8::String;
using v8::UnboundScript;
using v8::Value;

// static
VmRealm* VmRealm::New(Realm* creation_realm) {
  VmRealm* realm = new VmRealm(creation_realm);
  // TODO(legendecas): required by node::PromiseRejectCallback.
  // Remove this once promise rejection doesn't need to be handled across
  // realms.
  realm->context()->SetSecurityToken(
      creation_realm->context()->GetSecurityToken());

  // We do not expect the realm bootstrapping to throw any
  // exceptions. If it does, exit the current Node.js instance.
  TryCatchScope try_catch(creation_realm->env(),
                          TryCatchScope::CatchMode::kFatal);
  if (realm->RunBootstrapping().IsEmpty()) {
    delete realm;
    return nullptr;
  }
  return realm;
}

// static
void VmRealm::WeakCallback(const v8::WeakCallbackInfo<VmRealm>& data) {
  VmRealm* realm = data.GetParameter();
  realm->context_.Reset();

  // Yield to pending weak callbacks before deleting the realm.
  // This is necessary to avoid cleaning up base objects before their scheduled
  // weak callbacks are invoked, which can lead to accessing to v8 apis during
  // the first pass of the weak callback.
  realm->env()->SetImmediate([realm](Environment* env) { delete realm; });
  // Remove the cleanup hook to avoid deleting the realm again.
  realm->env()->RemoveCleanupHook(DeleteMe, realm);
}

// static
void VmRealm::DeleteMe(void* data) {
  VmRealm* realm = static_cast<VmRealm*>(data);
  // Clear the context handle to avoid invoking the weak callback again.
  // Also, the context internal slots are cleared and the context is no longer
  // reference to the realm.
  delete realm;
}

VmRealm::VmRealm(Realm* creation_realm)
    : Realm(creation_realm->env(),
            NewContext(creation_realm->isolate()),
            kVmRealm),
      creation_realm_(creation_realm) {
  // TODO(legendecas): build realm dependency graph before allowing creating
  // VmRealm in arbitrary realms.
  CHECK_EQ(creation_realm->kind(), kPrincipal);

  CreateProperties();
  env_->TrackVmRealm(this);
  env_->AddCleanupHook(DeleteMe, this);
}

VmRealm::~VmRealm() {
  while (HasCleanupHooks()) {
    RunCleanup();
  }

  env_->UntrackVmRealm(this);

  if (context_.IsEmpty()) {
    // This most likely happened because the weak callback cleared it.
    return;
  }

  {
    HandleScope handle_scope(isolate());
    env_->UnassignFromContext(context());
  }
}

v8::Local<v8::Context> VmRealm::context() const {
  Local<Context> ctx = PersistentToLocal::Default(isolate_, context_);
  DCHECK(!ctx.IsEmpty());
  return ctx;
}

void VmRealm::Stop() {
  context_.SetWeak(this, WeakCallback, v8::WeakCallbackType::kParameter);
  while (HasCleanupHooks()) {
    RunCleanup();
  }
}

// V8 can not infer reference cycles between global persistent handles, e.g.
// the Realm's Context handle and the per-realm function handles.
// Attach the per-realm strong persistent values' lifetime to the context's
// global object to avoid the strong global references to the per-realm objects
// keep the context alive indefinitely.
#define V(PropertyName, TypeName)                                              \
  v8::Local<TypeName> VmRealm::PropertyName() const {                          \
    return PersistentToLocal::Default(isolate_, PropertyName##_);              \
  }                                                                            \
  void VmRealm::set_##PropertyName(v8::Local<TypeName> value) {                \
    HandleScope scope(isolate_);                                               \
    PropertyName##_.Reset(isolate_, value);                                    \
    v8::Local<v8::Context> ctx = context();                                    \
    if (value.IsEmpty()) {                                                     \
      ctx->Global()                                                            \
          ->SetPrivate(ctx,                                                    \
                       isolate_data()->per_realm_##PropertyName(),             \
                       v8::Undefined(isolate_))                                \
          .ToChecked();                                                        \
    } else {                                                                   \
      PropertyName##_.SetWeak();                                               \
      ctx->Global()                                                            \
          ->SetPrivate(ctx, isolate_data()->per_realm_##PropertyName(), value) \
          .ToChecked();                                                        \
    }                                                                          \
  }
PER_REALM_STRONG_PERSISTENT_VALUES(V)
#undef V

v8::MaybeLocal<v8::Value> VmRealm::BootstrapRealm() {
  HandleScope scope(isolate_);

  // Skip "internal/bootstrap/node" as it installs node globals and per-isolate
  // callbacks.

  if (!env_->no_browser_globals()) {
    if (ExecuteBootstrapper("internal/bootstrap/web/exposed-wildcard")
            .IsEmpty() ||
        ExecuteBootstrapper("internal/bootstrap/web/exposed-window-or-worker")
            .IsEmpty()) {
      return MaybeLocal<Value>();
    }
  }

  // The process object is not exposed globally in ShadowRealm yet.
  // However, the process properties need to be setup for built-in modules.
  // Specifically, process.cwd() is needed by the ESM loader.
  if (ExecuteBootstrapper(
          "internal/bootstrap/switches/does_not_own_process_state")
          .IsEmpty()) {
    return MaybeLocal<Value>();
  }

  // Setup process.env proxy.
  Local<String> env_string = FIXED_ONE_BYTE_STRING(isolate_, "env");
  Local<Object> env_proxy;
  if (!isolate_data()->env_proxy_template()->NewInstance(context()).ToLocal(
          &env_proxy) ||
      process_object()->Set(context(), env_string, env_proxy).IsNothing()) {
    return MaybeLocal<Value>();
  }

  // TODO(legendecas): XXX
  if (ExecuteBootstrapper("internal/bootstrap/shadow_realm").IsEmpty()) {
    return MaybeLocal<Value>();
  }

  return v8::True(isolate_);
}

MaybeLocal<Value> VmRealm::ImportModuleDynamically(
    Local<String> specifier, Local<Object> import_attributes) {
  Local<Context> ctx = context();
  EscapableHandleScope handle_scope(isolate());

  Local<Function> import_callback = host_import_module_dynamically_callback();
  Local<Value> id =
      ctx->Global()
          ->GetPrivate(ctx, isolate_data()->host_defined_option_symbol())
          .ToLocalChecked();

  Local<Value> import_args[] = {
      id,
      Local<Value>(specifier),
      import_attributes,
  };

  Local<Value> result;
  if (import_callback
          ->Call(ctx, Undefined(isolate()), arraysize(import_args), import_args)
          .ToLocal(&result)) {
    CHECK(result->IsPromise());
    return handle_scope.Escape(result);
  }

  return MaybeLocal<Value>();
}

// static
void VmRealmWrapper::CreatePerIsolateProperties(IsolateData* isolate_data,
                                                Local<ObjectTemplate> target) {
  Isolate* isolate = isolate_data->isolate();
  Local<String> class_name = FIXED_ONE_BYTE_STRING(isolate, "VmRealm");

  Local<FunctionTemplate> tmpl = NewFunctionTemplate(isolate, New);
  tmpl->InstanceTemplate()->SetInternalFieldCount(
      VmRealmWrapper::kInternalFieldCount);
  tmpl->SetClassName(class_name);
  SetProtoMethod(isolate, tmpl, "stop", Stop);
  SetProtoMethod(isolate, tmpl, "import", Import);
  SetProtoMethod(isolate, tmpl, "evaluate", Evaluate);

  target->Set(isolate, "VmRealm", tmpl);
  isolate_data->set_vm_realm_constructor_template(tmpl);
}

// static
void VmRealmWrapper::RegisterExternalReferences(
    ExternalReferenceRegistry* registry) {
  registry->Register(New);
  registry->Register(Stop);
  registry->Register(Import);
  registry->Register(Evaluate);
}

// static
void VmRealmWrapper::New(const v8::FunctionCallbackInfo<v8::Value>& args) {
  Realm* realm = Realm::GetCurrent(args);
  Isolate* isolate = realm->isolate();

  VmRealmWrapper* wrapper = new VmRealmWrapper(realm, args.This());

  if (args.This()
          ->Set(realm->context(),
                FIXED_ONE_BYTE_STRING(isolate, "globalThis"),
                wrapper->vm_realm_->context()->Global())
          .IsNothing())
    return;

  USE(wrapper);
}

// static
void VmRealmWrapper::Evaluate(const v8::FunctionCallbackInfo<v8::Value>& args) {
  Environment* env = Environment::GetCurrent(args);

  VmRealmWrapper* wrapper;
  ASSIGN_OR_RETURN_UNWRAP(&wrapper, args.This());

  const int argc = args.Length();
  CHECK_EQ(argc, 1);

  if (!ContextifyScript::InstanceOf(env, args[0])) {
    THROW_ERR_INVALID_ARG_TYPE(
        env, "Script methods can only be called on script instances.");
    return;
  }
  ContextifyScript* wrapped_script;
  ASSIGN_OR_RETURN_UNWRAP(&wrapped_script, args[0]);

  MaybeLocal<Value> result = wrapped_script->EvalMachine(
      wrapper->vm_realm_->context(),
      env,
      -1 /* timeout */,
      false /* display_errors */,
      false /* break_on_sigint */,
      false /* break_on_first_line */,
      wrapper->vm_realm_->context()->GetMicrotaskQueue());
  if (!result.IsEmpty()) {
    args.GetReturnValue().Set(result.ToLocalChecked());
  }
}

// static
void VmRealmWrapper::Import(const v8::FunctionCallbackInfo<v8::Value>& args) {
  VmRealmWrapper* wrapper;
  ASSIGN_OR_RETURN_UNWRAP(&wrapper, args.This());

  const int argc = args.Length();
  CHECK_EQ(argc, 2);

  CHECK(args[0]->IsString());
  Local<String> specifier = args[0].As<String>();

  Local<Object> import_attributes = args[1].As<Object>();

  MaybeLocal<Value> result =
      wrapper->vm_realm_->ImportModuleDynamically(specifier, import_attributes);
  if (!result.IsEmpty()) {
    args.GetReturnValue().Set(result.ToLocalChecked());
  }
}

// static
void VmRealmWrapper::Stop(const v8::FunctionCallbackInfo<v8::Value>& args) {
  VmRealmWrapper* wrapper;
  ASSIGN_OR_RETURN_UNWRAP(&wrapper, args.This());

  wrapper->vm_realm_->Stop();
  wrapper->signaled_stop_ = true;
}

VmRealmWrapper::VmRealmWrapper(Realm* creation_realm,
                               v8::Local<v8::Object> wrapper)
    : BaseObject(creation_realm, wrapper) {
  vm_realm_ = VmRealm::New(creation_realm);

  MakeWeak();
}

void VmRealmWrapper::MemoryInfo(MemoryTracker* tracker) const {
  // TODO: implement
}

}  // namespace node
