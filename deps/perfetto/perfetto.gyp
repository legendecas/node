{
  "variables": {
    "GN-scrapper": "../../tools/v8_gypfiles/GN-scraper",
    "perfetto_root": "./",
  },
  "targets": [
    {
      'target_name': 'libperfetto',
      'type': 'static_library',
      'cflags': ['-fvisibility=hidden'],
      'xcode_settings': {
        'GCC_SYMBOLS_PRIVATE_EXTERN': 'YES',  # -fvisibility=hidden
      },
      'dependencies': [
        '../protobuf/protobuf.gyp:protobuf-lite',
        '../protobuf/protobuf.gyp:protoc',
        # ':ipc_plugin',
        # ':protozero_plugin',
        # ':cppgen_plugin',
        # ':protoc-gen',
        '../zlib/zlib.gyp:zlib',
      ],
      'include_dirs': [
        'config',
        '<@(SHARED_INTERMEDIATE_DIR)/perfetto/protozero',
        '<@(SHARED_INTERMEDIATE_DIR)/perfetto/cppgen',
        '<@(SHARED_INTERMEDIATE_DIR)/perfetto/cpp',
        'include',
        'src',
      ],
      'direct_dependent_settings': {
        'include_dirs': [
          'include',
        ]
      },
      'defines': [
        'GOOGLE_PROTOBUF_NO_RTTI',
        'GOOGLE_PROTOBUF_NO_STATIC_INITIALIZER',
      ],
      'sources': [
        # include/perfetto/base
        '<!@pymod_do_main(<(GN-scrapper) "<(perfetto_root)/include/perfetto/base/BUILD.gn" "\"base.*?sources = ")',
        # include/perfetto/public:base
        '<!@pymod_do_main(<(GN-scrapper) "<(perfetto_root)/include/perfetto/public/BUILD.gn" "\"base.*?sources = ")',
        # include/perfetto/tracing
        '<!@pymod_do_main(<(GN-scrapper) "<(perfetto_root)/include/perfetto/tracing/BUILD.gn" "\"tracing.*?sources = ")',
        '<!@pymod_do_main(<(GN-scrapper) "<(perfetto_root)/include/perfetto/tracing/BUILD.gn" "\"forward_decls.*?sources = ")',
        # include/perfetto/tracing/core
        '<!@pymod_do_main(<(GN-scrapper) "<(perfetto_root)/include/perfetto/tracing/core/BUILD.gn" "\"core.*?sources = ")',
        '<!@pymod_do_main(<(GN-scrapper) "<(perfetto_root)/include/perfetto/tracing/core/BUILD.gn" "\"forward_decls.*?sources = ")',

        # base
        '<!@pymod_do_main(<(GN-scrapper) "<(perfetto_root)/src/base/BUILD.gn" "\"base.*?sources = ")',
        # base:clock_snapshots
        '<!@pymod_do_main(<(GN-scrapper) "<(perfetto_root)/src/base/BUILD.gn" "\"clock_snapshots.*?sources = ")',
        # base:version
        '<!@pymod_do_main(<(GN-scrapper) "<(perfetto_root)/src/base/BUILD.gn" "\"version.*?sources = ")',

        # trace_processor/importers/memory_tracker:graph_processor
        '<!@pymod_do_main(<(GN-scrapper) "<(perfetto_root)/src/trace_processor/importers/memory_tracker/BUILD.gn" "\"graph_processor.*?sources = ")',

        # tracing:client_api_without_backends
        '<!@pymod_do_main(<(GN-scrapper) "<(perfetto_root)/src/tracing/BUILD.gn" "\"client_api_without_backends.*?sources = ")',
        # tracing:in_process_backend
        '<!@pymod_do_main(<(GN-scrapper) "<(perfetto_root)/src/tracing/BUILD.gn" "\"in_process_backend.*?sources = ")',
        # tracing:system_backend_fake
        '<!@pymod_do_main(<(GN-scrapper) "<(perfetto_root)/src/tracing/BUILD.gn" "\"system_backend_fake.*?sources = ")',
        # tracing:common
        '<!@pymod_do_main(<(GN-scrapper) "<(perfetto_root)/src/tracing/BUILD.gn" "\"common.*?sources = ")',
        # tracing/core:core
        '<!@pymod_do_main(<(GN-scrapper) "<(perfetto_root)/src/tracing/core/BUILD.gn" "\"core.*?sources = ")',
        # tracing/service:service
        '<!@pymod_do_main(<(GN-scrapper) "<(perfetto_root)/src/tracing/service/BUILD.gn" "\"service.*?sources = ")',

        # protozero
        # protozero/filtering:message_filter
        # protozero/filtering:string_filter

        # android_stats
        '<!@pymod_do_main(<(GN-scrapper) "<(perfetto_root)/src/android_stats/BUILD.gn" "\"android_stats.*?sources = ")',
        # android_stats:perfetto_atoms
        '<!@pymod_do_main(<(GN-scrapper) "<(perfetto_root)/src/android_stats/BUILD.gn" "\"perfetto_atoms.*?sources = ")',

        # protos/perfetto/common:zero
        # protos/perfetto/common:cpp
        # protos/perfetto/config:zero
        # protos/perfetto/config:cpp
        # protos/perfetto/config/interceptors:cpp
        # protos/perfetto/config/track_event:cpp
        # protos/perfetto/trace:zero
        # protos/perfetto/trace/perfetto:zero
      ]
    },
  ]
}
