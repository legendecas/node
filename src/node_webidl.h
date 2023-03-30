#ifndef SRC_NODE_WEBIDL
#define SRC_NODE_WEBIDL

#include "base_object.h"
#include "node_realm.h"

namespace node {
namespace webidl {

// Mixin of WebIDL's platform object.
class PlatformObject : public BaseObject {
 public:
  static void New(const v8::FunctionCallbackInfo<v8::Value>& args);

  PlatformObject(Realm* realm, v8::Local<v8::Object> object);
  SET_MEMORY_INFO_NAME(PlatformObject)
  SET_SELF_SIZE(PlatformObject)
  SET_NO_MEMORY_INFO()
};

}  // namespace webidl
}  // namespace node

#endif  // SRC_NODE_WEBIDL
