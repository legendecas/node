#ifndef SRC_TRACING_TRACE_EVENT_PERFETTO_H_
#define SRC_TRACING_TRACE_EVENT_PERFETTO_H_

#if !defined(V8_USE_PERFETTO)
#error Perfetto is not enabled.
#endif

// For now most of Node.js uses legacy trace events.
#define PERFETTO_ENABLE_LEGACY_TRACE_EVENTS 1

#include "perfetto/tracing/track_event.h"
#include "perfetto/tracing/track_event_legacy.h"

#define TRACING_CATEGORY_NODE "node"
#define TRACING_CATEGORY_NODE1(one)                                           \
    TRACING_CATEGORY_NODE "." #one
#define TRACING_CATEGORY_NODE2(one, two)                                      \
    TRACING_CATEGORY_NODE "." #one "." #two

// List of categories used by built-in Node.js trace events.
// clang-format off
PERFETTO_DEFINE_CATEGORIES_IN_NAMESPACE(
    node,
    perfetto::Category("__metadata"), // TODO: remove this
    perfetto::Category("node"),
    perfetto::Category("node.async_hooks"),
    perfetto::Category("node.environment"),
    perfetto::Category("node.realm"),
    perfetto::Category("node.bootstrap"),
    perfetto::Category("node.dns.native"),
    perfetto::Category("node.net.native"),
    perfetto::Category("node.vm.script"),
    perfetto::Category("node.fs_dir.sync"),
    perfetto::Category("node.fs_dir.async"),
    perfetto::Category("node.fs.sync"),
    perfetto::Category("node.fs.async"),
    perfetto::Category("node.perf.event_loop"),
    perfetto::Category("node.promises.rejections"),
    perfetto::Category("node.threadpoolwork.sync"),
    perfetto::Category("node.threadpoolwork.async"),
  );
// clang-format on

PERFETTO_USE_CATEGORIES_FROM_NAMESPACE(node);

#endif  // SRC_TRACING_TRACE_EVENT_PERFETTO_H_
