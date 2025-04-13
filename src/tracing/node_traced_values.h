#ifndef SRC_TRACING_NODE_TRACED_VALUES_H_
#define SRC_TRACING_NODE_TRACED_VALUES_H_

#include <span>
#include <string>

#include "perfetto/tracing/traced_value.h"

namespace node::tracing {

class EnvironmentArgs {
 public:
  EnvironmentArgs(std::span<const std::string> args,
                  std::span<const std::string> exec_args)
      : args_(args), exec_args_(exec_args) {}

  void WriteIntoTrace(perfetto::TracedValue context) const {
    auto dict = std::move(context).WriteDictionary();
    auto args_array = dict.AddArray("args");
    for (const auto& arg : args_) {
      args_array.Append(arg);
    }
    auto exec_args_array = dict.AddArray("exec_args");
    for (const auto& arg : exec_args_) {
      exec_args_array.Append(arg);
    }
  }

 private:
  std::span<const std::string> args_;
  std::span<const std::string> exec_args_;
};

class AsyncWrapArgs {
  public:
  AsyncWrapArgs(int64_t execution_async_id,
                   int64_t trigger_async_id)
       : execution_async_id_(execution_async_id), trigger_async_id_(trigger_async_id) {}

   void WriteIntoTrace(perfetto::TracedValue context) const {
    printf("AsyncWrapArgs::WriteIntoTrace\n");
     auto dict = std::move(context).WriteDictionary();
     dict.Add("executionAsyncId", execution_async_id_);
     dict.Add("triggerAsyncId", trigger_async_id_);
     dict.Add("foo", "bar");
   }

  private:
  int64_t execution_async_id_;
  int64_t trigger_async_id_;
 };


}

#endif  // SRC_TRACING_NODE_TRACED_VALUES_H_
