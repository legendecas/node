#include "node_shadow_realm.h"
#include "cppgc/allocation.h"
#include "env-inl.h"
#include "node_errors.h"
#include "node_process.h"

namespace node {
namespace shadow_realm {
using v8::Context;
using v8::EscapableHandleScope;
using v8::HandleScope;
using v8::Isolate;
using v8::Local;
using v8::MaybeLocal;
using v8::Object;
using v8::String;
using v8::Value;

using TryCatchScope = node::errors::TryCatchScope;

// static
ShadowRealm* ShadowRealm::New(Environment* env) {
  Isolate* isolate = env->isolate();
  ShadowRealm* realm = cppgc::MakeGarbageCollected<ShadowRealm>(
      isolate->GetCppHeap()->GetAllocationHandle(), env);
  // TODO(legendecas): required by node::PromiseRejectCallback.
  // Remove this once promise rejection doesn't need to be handled across
  // realms.
  realm->context()->SetSecurityToken(
      env->principal_realm()->context()->GetSecurityToken());

  // We do not expect the realm bootstrapping to throw any
  // exceptions. If it does, exit the current Node.js instance.
  TryCatchScope try_catch(env, TryCatchScope::CatchMode::kFatal);
  if (realm->RunBootstrapping().IsEmpty()) {
    delete realm;
    return nullptr;
  }
  return realm;
}

// static
MaybeLocal<Context> HostCreateShadowRealmContextCallback(
    Local<Context> initiator_context) {
  Environment* env = Environment::GetCurrent(initiator_context);
  EscapableHandleScope scope(env->isolate());

  // We do not expect the realm bootstrapping to throw any
  // exceptions. If it does, exit the current Node.js instance.
  TryCatchScope try_catch(env, TryCatchScope::CatchMode::kFatal);
  ShadowRealm* realm = ShadowRealm::New(env);
  if (realm != nullptr) {
    return scope.Escape(realm->context());
  }
  return MaybeLocal<Context>();
}

ShadowRealm::ShadowRealm(Environment* env)
    : Realm(env, NewContext(env->isolate()), kShadowRealm) {
  Isolate* isolate = env->isolate();
  HandleScope scope(isolate);
  Context::Scope context_scope(context());
  // Wrap `this` to the context global object to bind the lifetime to the
  // context.
  Object::Wrap<v8::CppHeapPointerTag::kDefaultTag>(
      isolate, context()->Global(), this);
  CreateProperties();

  env->TrackShadowRealm(this);
  env->cleanable_queue()->PushFront(this);
}

ShadowRealm::~ShadowRealm() {
  // The destructor can be invoked by the cppgc garbage collector. It is unsafe
  // to access any objects here.
}

void ShadowRealm::Prefinalize() {
  if (cleanable_queue_.IsEmpty()) {
    // This has been cleaned with an Environment cleanup.
    return;
  }
  // Cleanup native handles.
  Clean();
  cleanable_queue_.Remove();
}

void ShadowRealm::Clean() {
  while (PendingCleanup()) {
    RunCleanup();
  }
  env_->UntrackShadowRealm(this);
}

void ShadowRealm::Trace(cppgc::Visitor* visitor) const {
  Realm::Trace(visitor);
}

v8::Local<v8::Context> ShadowRealm::context() const {
  Local<Context> ctx = context_.Get(isolate_);
  DCHECK(!ctx.IsEmpty());
  return ctx;
}

// Per-realm strong value accessors. The per-realm values should avoid being
// accessed across realms.
#define V(PropertyName, TypeName)                                              \
  v8::Local<TypeName> ShadowRealm::PropertyName() const {                      \
    return PropertyName##_.Get(isolate_);                                      \
  }                                                                            \
  void ShadowRealm::set_##PropertyName(v8::Local<TypeName> value) {            \
    DCHECK_IMPLIES(!value.IsEmpty(),                                           \
                   isolate()->GetCurrentContext() == context());               \
    PropertyName##_.Reset(isolate(), value);                                   \
  }
PER_REALM_STRONG_PERSISTENT_VALUES(V)
#undef V

v8::MaybeLocal<v8::Value> ShadowRealm::BootstrapRealm() {
  HandleScope scope(isolate_);

  // Skip "internal/bootstrap/node" as it installs node globals and per-isolate
  // callbacks.

  if (!env_->no_browser_globals()) {
    if (ExecuteBootstrapper("internal/bootstrap/web/exposed-wildcard")
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

  if (ExecuteBootstrapper("internal/bootstrap/shadow_realm").IsEmpty()) {
    return MaybeLocal<Value>();
  }

  return v8::True(isolate_);
}

}  // namespace shadow_realm
}  // namespace node
