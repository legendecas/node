#ifndef SRC_NODE_VM_REALM_H_
#define SRC_NODE_VM_REALM_H_

#if defined(NODE_WANT_INTERNALS) && NODE_WANT_INTERNALS

#include "base_object-inl.h"
#include "node_context_data.h"
#include "node_errors.h"
#include "node_realm.h"

namespace node {
class ExternalReferenceRegistry;

class VmRealm : public Realm {
 public:
  static VmRealm* New(Realm* creation_realm);

  SET_MEMORY_INFO_NAME(VmRealm)
  SET_SELF_SIZE(VmRealm)

  v8::Local<v8::Context> context() const override;

#define V(PropertyName, TypeName)                                              \
  v8::Local<TypeName> PropertyName() const override;                           \
  void set_##PropertyName(v8::Local<TypeName> value) override;
  PER_REALM_STRONG_PERSISTENT_VALUES(V)
#undef V

  v8::MaybeLocal<v8::Value> ImportModuleDynamically(
      v8::Local<v8::String> specifier, v8::Local<v8::Object> import_attributes);
  void Stop();

 protected:
  v8::MaybeLocal<v8::Value> BootstrapRealm() override;

 private:
  static void WeakCallback(const v8::WeakCallbackInfo<VmRealm>& data);
  static void DeleteMe(void* data);

  explicit VmRealm(Realm* creation_realm);
  ~VmRealm() override;

  Realm* creation_realm_;
};

/**
 * VmRealmWrapper
 *  - (strong reference) VmRealm
 *     - (strong reference) v8::Context
 *
 * After the VmRealmWrapper::Stop call,
 * VmRealmWrapper
 *  - (strong reference) VmRealm
 *     - (weak reference) v8::Context
 *
 * If there are any reference to the objects created in the vm realm (either by
 * the parent realm, in realm handles), the context will not be garbage
 * collected. The VmRealmWrapper can be garbage collected, but the VmRealm will
 * not be. To release the VmRealm, both VmRealmWrapper and objects created in
 * the realm must be released.
 */
class VmRealmWrapper : public BaseObject {
 public:
  enum InternalFields {
    kContextSlot = BaseObject::kInternalFieldCount,
    kInternalFieldCount
  };

  VmRealmWrapper(Realm* creation_realm, v8::Local<v8::Object> wrapper);
  ~VmRealmWrapper() = default;

  void MemoryInfo(MemoryTracker* tracker) const override;
  SET_MEMORY_INFO_NAME(VmRealmWrapper)
  SET_SELF_SIZE(VmRealmWrapper)

  static void CreatePerIsolateProperties(IsolateData* isolate_data,
                                         v8::Local<v8::ObjectTemplate> target);
  static void RegisterExternalReferences(ExternalReferenceRegistry* registry);

  static void New(const v8::FunctionCallbackInfo<v8::Value>& args);
  static void Stop(const v8::FunctionCallbackInfo<v8::Value>& args);
  static void Evaluate(const v8::FunctionCallbackInfo<v8::Value>& args);
  static void Import(const v8::FunctionCallbackInfo<v8::Value>& args);

 private:
  VmRealm* vm_realm_;
  v8::Global<v8::Context> context_;
  bool signaled_stop_ = false;
};

}  // namespace node

#endif  // defined(NODE_WANT_INTERNALS) && NODE_WANT_INTERNALS

#endif  // SRC_NODE_VM_REALM_H_
