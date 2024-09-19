#ifndef SRC_NODE_SHADOW_REALM_H_
#define SRC_NODE_SHADOW_REALM_H_

#if defined(NODE_WANT_INTERNALS) && NODE_WANT_INTERNALS

#include "cppgc/prefinalizer.h"
#include "env.h"
#include "node_realm.h"
#include "v8.h"

namespace node {
namespace shadow_realm {

class ShadowRealm final : public cppgc::GarbageCollected<ShadowRealm>,
                          public cppgc::NameProvider,
                          public Realm,
                          public Cleanable {
  CPPGC_USING_PRE_FINALIZER(ShadowRealm, Prefinalize);

 public:
  static ShadowRealm* New(Environment* env);

  explicit ShadowRealm(Environment* env);
  ~ShadowRealm();

  SET_MEMORY_INFO_NAME(ShadowRealm)
  SET_SELF_SIZE(ShadowRealm)

  SET_CPPGC_NAME(ShadowRealm)
  void Trace(cppgc::Visitor* visitor) const final;

  v8::Local<v8::Context> context() const override;

#define V(PropertyName, TypeName)                                              \
  v8::Local<TypeName> PropertyName() const override;                           \
  void set_##PropertyName(v8::Local<TypeName> value) override;
  PER_REALM_STRONG_PERSISTENT_VALUES(V)
#undef V

 protected:
  v8::MaybeLocal<v8::Value> BootstrapRealm() override;

 private:
  void Prefinalize();
  // This must be invoked outside of the destructor, which is invoked during
  // cppgc gc phase.
  void Clean() override;
};

v8::MaybeLocal<v8::Context> HostCreateShadowRealmContextCallback(
    v8::Local<v8::Context> initiator_context);

}  // namespace shadow_realm
}  // namespace node

#endif  // defined(NODE_WANT_INTERNALS) && NODE_WANT_INTERNALS

#endif  // SRC_NODE_SHADOW_REALM_H_
