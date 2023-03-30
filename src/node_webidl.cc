#include "node_webidl.h"
#include "env-inl.h"
#include "node_binding.h"
#include "node_external_reference.h"
#include "node_realm-inl.h"

namespace node {
namespace webidl {
using v8::Context;
using v8::FunctionTemplate;
using v8::Isolate;
using v8::Local;
using v8::Object;
using v8::ObjectTemplate;
using v8::Value;

// static
void PlatformObject::New(const v8::FunctionCallbackInfo<v8::Value>& args) {
  Realm* realm = Realm::GetCurrent(args);
  Local<Object> self = args.This();
  new PlatformObject(realm, self);
}

PlatformObject::PlatformObject(Realm* realm, v8::Local<v8::Object> object)
    : BaseObject(realm, object) {
  MakeWeak();
}

void CreatePerIsolateProperties(IsolateData* isolate_data,
                                Local<FunctionTemplate> target) {
  Isolate* isolate = isolate_data->isolate();
  Local<ObjectTemplate> proto = target->PrototypeTemplate();

  Local<FunctionTemplate> tpl =
      NewFunctionTemplate(isolate, PlatformObject::New);
  tpl->InstanceTemplate()->SetInternalFieldCount(
      BaseObject::kInternalFieldCount);
  // Platform object is a mixin. Do not install any prototype methods.

  isolate_data->set_platform_object_template(tpl);
  SetConstructorFunction(
      isolate, proto, FIXED_ONE_BYTE_STRING(isolate, "PlatformObject"), tpl);
}

void CreatePerContextProperties(Local<Object> target,
                                Local<Value> unused,
                                Local<Context> context,
                                void* priv) {
  // Nothing to be done.
}

void RegisterExternalReferences(ExternalReferenceRegistry* registry) {
  registry->Register(PlatformObject::New);
}

}  // namespace webidl
}  // namespace node

NODE_BINDING_CONTEXT_AWARE_INTERNAL(webidl,
                                    node::webidl::CreatePerContextProperties)
NODE_BINDING_PER_ISOLATE_INIT(webidl, node::webidl::CreatePerIsolateProperties)
NODE_BINDING_EXTERNAL_REFERENCE(webidl,
                                node::webidl::RegisterExternalReferences)
