{
  'variables': {
    'perfetto_root': './',
    'perfetto_gen_root': '<(SHARED_INTERMEDIATE_DIR)/perfetto',
    'protobuf_gyp_file': '../protobuf/protobuf.gyp',
    'zlib_gyp_file': '../zlib/zlib.gyp',
    'absl_gyp_file': '../../tools/v8_gypfiles/abseil.gyp',
    'protoc_exec': '<(PRODUCT_DIR)/<(EXECUTABLE_PREFIX)protoc<(EXECUTABLE_SUFFIX)',
    'protozero_plugin_exec': '<(PRODUCT_DIR)/<(EXECUTABLE_PREFIX)protozero_plugin<(EXECUTABLE_SUFFIX)',
    'cppgen_plugin_exec': '<(PRODUCT_DIR)/<(EXECUTABLE_PREFIX)cppgen_plugin<(EXECUTABLE_SUFFIX)',
    'trace_processor_proto_files': [
      # deps/perfetto/protos/perfetto/trace_processor/proto_files.gni
      './protos/perfetto/trace_processor/metatrace_categories.proto',
      './protos/perfetto/trace_processor/serialization.proto',
      './protos/perfetto/trace_processor/stack.proto',
      './protos/perfetto/trace_processor/trace_processor.proto',
    ],
    'proto_cpp_files': [
      # Generates .gen.h and .gen.cc, and does not depend on `protobuf_lite` nor `protobuf_full`.
      '<!@pymod_do_main(GN-scraper "<(perfetto_root)/protos/perfetto/common/BUILD.gn" "sources = ")',
      '<!@pymod_do_main(GN-scraper "<(perfetto_root)/protos/perfetto/config/BUILD.gn" "sources = ")',
      '<!@pymod_do_main(GN-scraper "<(perfetto_root)/protos/perfetto/config/android/BUILD.gn" "sources = ")',
      '<!@pymod_do_main(GN-scraper "<(perfetto_root)/protos/perfetto/config/ftrace/BUILD.gn" "sources = ")',
      '<!@pymod_do_main(GN-scraper "<(perfetto_root)/protos/perfetto/config/gpu/BUILD.gn" "sources = ")',
      '<!@pymod_do_main(GN-scraper "<(perfetto_root)/protos/perfetto/config/inode_file/BUILD.gn" "sources = ")',
      '<!@pymod_do_main(GN-scraper "<(perfetto_root)/protos/perfetto/config/interceptors/BUILD.gn" "sources = ")',
      '<!@pymod_do_main(GN-scraper "<(perfetto_root)/protos/perfetto/config/power/BUILD.gn" "sources = ")',
      '<!@pymod_do_main(GN-scraper "<(perfetto_root)/protos/perfetto/config/process_stats/BUILD.gn" "sources = ")',
      '<!@pymod_do_main(GN-scraper "<(perfetto_root)/protos/perfetto/config/profiling/BUILD.gn" "sources = ")',
      '<!@pymod_do_main(GN-scraper "<(perfetto_root)/protos/perfetto/config/statsd/BUILD.gn" "sources = ")',
      '<!@pymod_do_main(GN-scraper "<(perfetto_root)/protos/perfetto/config/sys_stats/BUILD.gn" "sources = ")',
      '<!@pymod_do_main(GN-scraper "<(perfetto_root)/protos/perfetto/config/system_info/BUILD.gn" "sources = ")',
      '<!@pymod_do_main(GN-scraper "<(perfetto_root)/protos/perfetto/config/track_event/BUILD.gn" "sources = ")',
      '<!@pymod_do_main(GN-scraper "<(perfetto_root)/protos/perfetto/trace/BUILD.gn" "proto_sources_minimal = ")',
      '<@(trace_processor_proto_files)',
    ],
    'proto_cpp_output_files': [
      '<!@pymod_do_main(string_replace . "<(perfetto_gen_root)/cpp" .proto .gen.h <@(proto_cpp_files))',
      '<!@pymod_do_main(string_replace . "<(perfetto_gen_root)/cpp" .proto .gen.cc <@(proto_cpp_files))',
    ],
    'proto_track_event_files': [
      '<!@pymod_do_main(GN-scraper "<(perfetto_root)/protos/perfetto/trace/track_event/BUILD.gn" "sources = ")',
    ],
    'proto_track_events_output_files': [
      '<(perfetto_gen_root)/cpp/protos/third_party/chromium/chrome_track_event.gen.cc',
      '<(perfetto_gen_root)/cpp/protos/third_party/chromium/chrome_track_event.gen.h',
      '<(perfetto_gen_root)/cpp/protos/perfetto/trace/android/android_track_event.gen.cc',
      '<(perfetto_gen_root)/cpp/protos/perfetto/trace/android/android_track_event.gen.h',
      '<!@pymod_do_main(string_replace . "<(perfetto_gen_root)/cpp" .proto .gen.h <@(proto_track_event_files))',
      '<!@pymod_do_main(string_replace . "<(perfetto_gen_root)/cpp" .proto .gen.cc <@(proto_track_event_files))',
    ],
    'proto_lite_files': [
      # Generates libproto lite file .pb.h and .pb.cc, and depends on `protobuf_lite`.
      '<!@pymod_do_main(GN-scraper "<(perfetto_root)/protos/perfetto/common/BUILD.gn" "sources = ")',
      '<!@pymod_do_main(GN-scraper "<(perfetto_root)/protos/perfetto/trace/BUILD.gn" "proto_sources_minimal = ")',
      '<!@pymod_do_main(GN-scraper "<(perfetto_root)/protos/perfetto/trace/track_event/BUILD.gn" "sources = ")',
      '<@(trace_processor_proto_files)',
    ],
    'proto_lite_output_files': [
      '<!@pymod_do_main(string_replace . "<(perfetto_gen_root)/lite" .proto .pb.h <@(proto_lite_files))',
      '<!@pymod_do_main(string_replace . "<(perfetto_gen_root)/lite" .proto .pb.cc <@(proto_lite_files))',
    ],
    'proto_zero_files': [
      # Generates header only proto file .pbzero.h and .pbzero.cc (empty).
      '<!@pymod_do_main(GN-scraper "<(perfetto_root)/protos/perfetto/common/BUILD.gn" "sources = ")',
      '<!@pymod_do_main(GN-scraper "<(perfetto_root)/protos/perfetto/config/BUILD.gn" "sources = ")',
      '<!@pymod_do_main(GN-scraper "<(perfetto_root)/protos/perfetto/trace/BUILD.gn" "proto_sources_non_minimal = ")',
      '<!@pymod_do_main(GN-scraper "<(perfetto_root)/protos/perfetto/trace/BUILD.gn" "proto_sources_minimal = ")',
      '<!@pymod_do_main(GN-scraper "<(perfetto_root)/protos/perfetto/trace/android/BUILD.gn" "sources = ")',
      '<!@pymod_do_main(GN-scraper "<(perfetto_root)/protos/perfetto/trace/chrome/BUILD.gn" "sources = ")',
      '<!@pymod_do_main(GN-scraper "<(perfetto_root)/protos/perfetto/trace/gpu/BUILD.gn" "sources = ")',
      '<!@pymod_do_main(GN-scraper "<(perfetto_root)/protos/perfetto/trace/perfetto/BUILD.gn" "sources = ")',
      '<!@pymod_do_main(GN-scraper "<(perfetto_root)/protos/perfetto/trace/profiling/BUILD.gn" "sources = ")',
      '<!@pymod_do_main(GN-scraper "<(perfetto_root)/protos/perfetto/trace/ps/BUILD.gn" "sources = ")',
      '<!@pymod_do_main(GN-scraper "<(perfetto_root)/protos/perfetto/trace/track_event/BUILD.gn" "sources = ")',
      '<!@pymod_do_main(GN-scraper "<(perfetto_root)/protos/perfetto/trace/interned_data/BUILD.gn" "sources = ")',
      '<@(trace_processor_proto_files)',
    ],
    'proto_zero_output_files': [
      '<!@pymod_do_main(string_replace . "<(perfetto_gen_root)/pbzero" .proto .pbzero.h <@(proto_zero_files))',
      '<!@pymod_do_main(string_replace . "<(perfetto_gen_root)/pbzero" .proto .pbzero.cc <@(proto_zero_files))',
    ],
    'table_header_py_files': [
      '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/trace_processor/tables/BUILD.gn" "tables_python.*?sources = ")',
    ],
  },
  'targets': [
    {
      'target_name': 'libperfetto',
      'type': 'static_library',
      'cflags': ['-fvisibility=hidden'],
      'xcode_settings': {
        'GCC_SYMBOLS_PRIVATE_EXTERN': 'YES',  # -fvisibility=hidden
      },
      'dependencies': [
        'perfetto_base',
        'gen_perfetto',
        'gen_perfetto_cc_proto_descriptor',
        '<(absl_gyp_file):abseil',
        '<(protobuf_gyp_file):protobuf_lite',
        '<(zlib_gyp_file):zlib',
      ],
      'include_dirs': [
        '<(perfetto_root)/include',
        '<(perfetto_root)',
        '<(perfetto_gen_root)/lite',
        '<(perfetto_gen_root)/tables',
      ],
      'export_dependent_settings': [
        'perfetto_base',
        'gen_perfetto',
      ],
      'direct_dependent_settings': {
        'include_dirs': [
          '<(perfetto_root)/include',
        ],
      },
      'sources': [
        # include/perfetto/public:base
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/include/perfetto/public/BUILD.gn" "\\"base.*?sources = ")',
        # include/perfetto/tracing
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/include/perfetto/tracing/BUILD.gn" "\\"tracing.*?sources = ")',
        # include/perfetto/tracing/core
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/include/perfetto/tracing/core/BUILD.gn" "\\"core.*?sources = ")',
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/include/perfetto/tracing/core/BUILD.gn" "\\"forward_decls.*?sources = ")',

        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/base/BUILD.gn" "!is_nacl.*?sources \\+= ")',
        # base:clock_snapshots
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/base/BUILD.gn" "\\"clock_snapshots.*?sources = ")',
        # base:version
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/base/BUILD.gn" "\\"version.*?sources = ")',
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/base/BUILD.gn" "\\"perfetto_base_default_platform.*?sources = ")',

        # trace_processor/importers/memory_tracker:graph_processor
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/trace_processor/importers/memory_tracker/BUILD.gn" "\\"graph_processor.*?sources = ")',
        # trace_processor/db:minimal
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/trace_processor/db/BUILD.gn" "\\"minimal.*?sources = ")',
        # trace_processor/db/column
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/trace_processor/db/column/BUILD.gn" "\\"column.*?sources = ")',
        # trace_processor/util
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/trace_processor/util/BUILD.gn" "\\"bump_allocator.*?sources = ")',
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/trace_processor/util/BUILD.gn" "\\"glob.*?sources = ")',
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/trace_processor/util/BUILD.gn" "\\"regex.*?sources = ")',
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/trace_processor/util/BUILD.gn" "\\"util.*?sources = ")',
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/trace_processor/util/BUILD.gn" "\\"descriptors.*?sources = ")',
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/trace_processor/util/BUILD.gn" "\\"gzip.*?sources = ")',
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/trace_processor/util/BUILD.gn" "\\"proto_to_args_parser.*?sources = ")',
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/trace_processor/util/BUILD.gn" "\\"trace_type.*?sources = ")',
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/trace_processor/util/BUILD.gn" "\\"profiler_util.*?sources = ")',
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/trace_processor/util/BUILD.gn" "\\"trace_blob_view_reader.*?sources = ")',
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/trace_processor/util/BUILD.gn" "\\"build_id.*?sources = ")',
        # trace_processor:storage_minimal
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/trace_processor/BUILD.gn" "\\"storage_minimal.*?sources = ")',
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/trace_processor/BUILD.gn" "\\"metatrace.*?sources = ")',
        # trace_processor/types
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/trace_processor/types/BUILD.gn" "\\"types.*?sources = ")',
        # trace_processor/containers
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/trace_processor/containers/BUILD.gn" "\\"containers.*?sources = ")',
        # trace_processor/importers/common
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/trace_processor/importers/common/BUILD.gn" "\\"common.*?sources = ")',
        # trace_processor/importers/etw
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/trace_processor/importers/etw/BUILD.gn" "\\"minimal.*?sources = ")',
        # trace_processor/importers/android_bugreport:android_log_event
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/trace_processor/importers/android_bugreport/BUILD.gn" "\\"android_dumpstate_event.*?sources = ")',
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/trace_processor/importers/android_bugreport/BUILD.gn" "\\"android_log_event.*?sources = ")',
        # trace_processor/importers/ftrace:minimal
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/trace_processor/importers/ftrace/BUILD.gn" "\\"minimal.*?sources = ")',
        # trace_processor/importers/fuchsia:fuchsia_record
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/trace_processor/importers/fuchsia/BUILD.gn" "\\"fuchsia_record.*?sources = ")',
        # trace_processor/importers/proto:minimal
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/trace_processor/importers/proto/BUILD.gn" "\\"minimal.*?sources = ")',
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/trace_processor/importers/proto/BUILD.gn" "\\"proto_importer_module.*?sources = ")',
        # trace_processor/importers/perf:record
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/trace_processor/importers/perf/BUILD.gn" "\\"record.*?sources = ")',
        # trace_processor/importers/perf_text
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/trace_processor/importers/perf_text/BUILD.gn" "\\"perf_text.*?sources = ")',
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/trace_processor/importers/perf_text/BUILD.gn" "\\"perf_text_sample_line_parser.*?sources = ")',
        # trace_processor/sorter
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/trace_processor/sorter/BUILD.gn" "\\"sorter.*?sources = ")',
        # trace_processor/storage
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/trace_processor/storage/BUILD.gn" "\\"storage.*?sources = ")',
        # trace_processor/tables
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/trace_processor/tables/BUILD.gn" "source_set.\\"tables\\".*?sources = ")',

        # tracing:client_api_without_backends
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/tracing/BUILD.gn" "\\"client_api_without_backends.*?sources = ")',
        # tracing:in_process_backend
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/tracing/BUILD.gn" "\\"in_process_backend.*?sources = ")',
        # tracing:system_backend_fake
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/tracing/BUILD.gn" "\\"system_backend_fake.*?sources = ")',
        # tracing:common
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/tracing/BUILD.gn" "\\"common.*?sources = ")',
        # tracing:platform_impl
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/tracing/BUILD.gn" "\\"platform_impl.*?sources = ")',
        # tracing/core:core
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/tracing/core/BUILD.gn" "\\"core.*?sources = ")',
        # tracing/service:service
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/tracing/service/BUILD.gn" "\\"service.*?sources = ")',

        # protozero
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/protozero/BUILD.gn" "\\"protozero.*?sources = ")',
        # protozero/filtering:message_filter
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/protozero/filtering/BUILD.gn" "\\"message_filter.*?sources = ")',
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/protozero/filtering/BUILD.gn" "\\"bytecode_parser.*?sources = ")',
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/protozero/filtering/BUILD.gn" "\\"bytecode_common.*?sources = ")',
        # protozero/filtering:string_filter
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/protozero/filtering/BUILD.gn" "\\"string_filter.*?sources = ")',

        # android_stats
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/android_stats/BUILD.gn" "\\"android_stats.*?sources = ")',
        # android_stats:perfetto_atoms
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/android_stats/BUILD.gn" "\\"perfetto_atoms.*?sources = ")',

        # protos/perfetto/common:zero
        # protos/perfetto/common:cpp
        # protos/perfetto/config:zero
        # protos/perfetto/config:cpp
        # protos/perfetto/config/interceptors:cpp
        # protos/perfetto/config/track_event:cpp
        # protos/perfetto/trace:zero
        # protos/perfetto/trace/perfetto:zero

        # Generated sources
        '<@(proto_cpp_output_files)',
        '<@(proto_track_events_output_files)',
        '<@(proto_zero_output_files)',
        '<@(proto_lite_output_files)',
      ],
    },
    {
      # Refer to deps/perfetto/gn/perfetto_cc_proto_descriptor.gni for options
      'target_name': 'gen_perfetto_cc_proto_descriptor',
      'type': 'none',
      'hard_dependency': 1,
      'dependencies': [
        'gen_perfetto'
      ],
      'direct_dependent_settings': {
        'include_dirs': [
          '<(perfetto_gen_root)/descriptor',
        ]
      },
      'actions': [
        {
          'action_name': 'gen_cc_chrome_track_event_descriptor',
          'inputs': [
            '<(perfetto_gen_root)/cpp/chrome_track_event.descriptor',
          ],
          'outputs': [
            '<(perfetto_gen_root)/descriptor/src/trace_processor/importers/proto/chrome_track_event.descriptor.h',
          ],
          'process_outputs_as_sources': 1,
          'action': [
            '<(python)',
            '<(perfetto_root)/tools/gen_cc_proto_descriptor.py',
            '--gen_dir',
            '<(perfetto_gen_root)/descriptor',
            '--cpp_out',
            '<@(_outputs)',
            '<@(_inputs)',
          ],
          'message': 'Generating cc chrome_track_event descriptor'
        },
        {
          'action_name': 'gen_cc_android_track_event_descriptor',
          'inputs': [
            '<(perfetto_gen_root)/cpp/android_track_event.descriptor',
          ],
          'outputs': [
            '<(perfetto_gen_root)/descriptor/src/trace_processor/importers/proto/android_track_event.descriptor.h',
          ],
          'process_outputs_as_sources': 1,
          'action': [
            '<(python)',
            '<(perfetto_root)/tools/gen_cc_proto_descriptor.py',
            '--gen_dir',
            '<(perfetto_gen_root)/descriptor',
            '--cpp_out',
            '<@(_outputs)',
            '<@(_inputs)',
          ],
          'message': 'Generating cc chrome_track_event descriptor'
        },
        {
          'action_name': 'gen_cc_track_event_descriptor',
          'inputs': [
            '<(perfetto_gen_root)/cpp/track_event.descriptor',
          ],
          'outputs': [
            '<(perfetto_gen_root)/descriptor/src/trace_processor/importers/proto/track_event.descriptor.h',
          ],
          'process_outputs_as_sources': 1,
          'action': [
            '<(python)',
            '<(perfetto_root)/tools/gen_cc_proto_descriptor.py',
            '--gen_dir',
            '<(perfetto_gen_root)/descriptor',
            '--cpp_out',
            '<@(_outputs)',
            '<@(_inputs)',
          ],
          'message': 'Generating cc track_event descriptor'
        },
      ],
    },
    {
      'target_name': 'gen_perfetto',
      'type': 'none',
      'hard_dependency': 1,
      'dependencies': [
        'protozero_plugin',
        'cppgen_plugin',
        '<(protobuf_gyp_file):protoc',
      ],
      'direct_dependent_settings': {
        'defines': [
          'GOOGLE_PROTOBUF_NO_RTTI',
          'GOOGLE_PROTOBUF_NO_STATIC_INITIALIZER',
        ],
        'include_dirs': [
          # For proto headers.
          # Do not expose <(perfetto_gen_root)/lite headers, which depend on `protobuf_lite` library.
          '<(perfetto_gen_root)/cpp',
          '<(perfetto_gen_root)/pbzero',
        ]
      },
      'actions': [
        {
          'action_name': 'gen_proto_cpp',
          'inputs': [
            '<@(proto_cpp_files)',
          ],
          'outputs': [
            '<@(proto_cpp_output_files)',
          ],
          'process_outputs_as_sources': 1,
          # Refer to deps/perfetto/gn/proto_library.gni for options
          'action': [
            '<(protoc_exec)',
            '--plugin=protoc-gen-plugin=<(cppgen_plugin_exec)',
            '--plugin_out=wrapper_namespace=gen:<(perfetto_gen_root)/cpp',
            '--proto_path',
            '<(perfetto_root)',
            '<@(proto_cpp_files)',
          ],
          'message': 'Generating proto cpp sources'
        },
        {
          'action_name': 'gen_proto_zero',
          'inputs': [
            '<@(proto_zero_files)',
          ],
          'outputs': [
            '<@(proto_zero_output_files)',
          ],
          'process_outputs_as_sources': 1,
          # Refer to deps/perfetto/gn/proto_library.gni for options
          'action': [
            '<(protoc_exec)',
            '--plugin=protoc-gen-plugin=<(protozero_plugin_exec)',
            '--plugin_out=wrapper_namespace=pbzero:<(perfetto_gen_root)/pbzero',
            '--proto_path',
            '<(perfetto_root)',
            '<@(proto_zero_files)',
          ],
          'message': 'Generating proto zero sources'
        },
        {
          'action_name': 'gen_proto_lite',
          'inputs': [
            '<@(proto_lite_files)',
          ],
          'outputs': [
            '<@(proto_lite_output_files)',
          ],
          'process_outputs_as_sources': 1,
          # Refer to deps/perfetto/gn/proto_library.gni for options
          'action': [
            '<(protoc_exec)',
            '--proto_path',
            '<(perfetto_root)',
            '--cpp_out',
            'lite=true:<(perfetto_gen_root)/lite',
            '<@(proto_lite_files)',
          ],
          'message': 'Generating proto lite sources'
        },
        {
          'action_name': 'gen_cc_chrome_track_event_descriptor',
          'inputs': [
            './protos/third_party/chromium/chrome_track_event.proto',
          ],
          'outputs': [
            '<(perfetto_gen_root)/cpp/protos/third_party/chromium/chrome_track_event.gen.h',
            '<(perfetto_gen_root)/cpp/protos/third_party/chromium/chrome_track_event.gen.cc',
            '<(perfetto_gen_root)/cpp/chrome_track_event.d',
            '<(perfetto_gen_root)/cpp/chrome_track_event.descriptor',
          ],
          'process_outputs_as_sources': 1,
          # Refer to deps/perfetto/protos/third_party/chromium/BUILD.gn for options
          'action': [
            '<(protoc_exec)',
            '--plugin=protoc-gen-plugin=<(cppgen_plugin_exec)',
            '--plugin_out=wrapper_namespace=gen:<(perfetto_gen_root)/cpp',
            '--proto_path',
            '<(perfetto_root)',
            '--descriptor_set_out',
            '<(perfetto_gen_root)/cpp/chrome_track_event.descriptor',
            '--dependency_out',
            '<(perfetto_gen_root)/cpp/chrome_track_event.d',
            '<@(_inputs)',
          ],
          'message': 'Generating proto chrome_track_event sources'
        },
        {
          'action_name': 'gen_cc_android_track_event_descriptor',
          'inputs': [
            './protos/perfetto/trace/android/android_track_event.proto',
          ],
          'outputs': [
            '<(perfetto_gen_root)/cpp/protos/perfetto/trace/android/android_track_event.gen.h',
            '<(perfetto_gen_root)/cpp/protos/perfetto/trace/android/android_track_event.gen.cc',
            '<(perfetto_gen_root)/cpp/android_track_event.d',
            '<(perfetto_gen_root)/cpp/android_track_event.descriptor',
          ],
          'process_outputs_as_sources': 1,
          # Refer to deps/perfetto/protos/perfetto/trace/android/BUILD.gn for options
          'action': [
            '<(protoc_exec)',
            '--plugin=protoc-gen-plugin=<(cppgen_plugin_exec)',
            '--plugin_out=wrapper_namespace=gen:<(perfetto_gen_root)/cpp',
            '--proto_path',
            '<(perfetto_root)',
            '--descriptor_set_out',
            '<(perfetto_gen_root)/cpp/android_track_event.descriptor',
            '--dependency_out',
            '<(perfetto_gen_root)/cpp/android_track_event.d',
            '<@(_inputs)',
          ],
          'message': 'Generating proto android_track_event sources'
        },
        {
          'action_name': 'gen_cc_track_event_descriptor',
          'inputs': [
            '<@(proto_track_event_files)',
          ],
          'outputs': [
            '<!@pymod_do_main(string_replace . "<(perfetto_gen_root)/cpp" .proto .gen.h <@(_inputs))',
            '<!@pymod_do_main(string_replace . "<(perfetto_gen_root)/cpp" .proto .gen.cc <@(_inputs))',
            '<(perfetto_gen_root)/cpp/track_event.d',
            '<(perfetto_gen_root)/cpp/track_event.descriptor',
          ],
          'process_outputs_as_sources': 1,
          # Refer to deps/perfetto/protos/perfetto/trace/track_event/BUILD.gn for options
          'action': [
            '<(protoc_exec)',
            '--plugin=protoc-gen-plugin=<(cppgen_plugin_exec)',
            '--plugin_out=wrapper_namespace=gen:<(perfetto_gen_root)/cpp',
            '--proto_path',
            '<(perfetto_root)',
            '--descriptor_set_out',
            '<(perfetto_gen_root)/cpp/track_event.descriptor',
            # '--dependency_out',
            # '<(perfetto_gen_root)/cpp/track_event.d',
            '<@(_inputs)',
          ],
          'message': 'Generating proto track_event sources'
        },
        {
          'action_name': 'gen_table_headers',
          'inputs': [

          ],
          'outputs': [
            '<!@pymod_do_main(string_replace . "<(perfetto_gen_root)/tables" .py _py.h <@(table_header_py_files))',
          ],
          'process_outputs_as_sources': 1,
          # Refer to deps/perfetto/gn/proto_library.gni for options
          'action': [
            '<(python)',
            'tools/gen_tp_table_headers.py',
            '--gen-dir',
            '<(perfetto_gen_root)/tables',
            '--inputs',
            '<!@pymod_do_main(rebase_path . <@(table_header_py_files))',
          ],
          'message': 'Generating storage table headers'
        },
      ],
    },
    {
      'target_name': 'perfetto_base',
      'type': 'static_library',
      'include_dirs': [
        '<(perfetto_root)/include',
        '<(perfetto_root)',
        '<(perfetto_gen_root)/base',
      ],
      'direct_dependent_settings': {
        'include_dirs': [
          '<(perfetto_gen_root)/base',
        ],
      },
      'sources': [
        # include/perfetto/base
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/include/perfetto/base/BUILD.gn" "\\"base.*?sources = ")',
        # base
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/base/BUILD.gn" "\\"base.*?sources = ")',
      ],
      'actions': [
        {
          'action_name': 'gen_buildflags',
          'inputs': [
            '<(perfetto_root)/gn/write_buildflag_header.py',
          ],
          'outputs': [
            '<@(perfetto_gen_root)/base/perfetto_build_flags.h',
          ],
          'process_outputs_as_sources': 1,
          'action': [
            '<(python)',
            '<(perfetto_root)gn/write_buildflag_header.py',
            "--out",
            "<(perfetto_gen_root)/base/perfetto_build_flags.h",
            "--rsp",
            '<!pymod_do_main(gen_buildflag \
              "--flags" \
              "PERFETTO_ANDROID_BUILD=false" \
              "PERFETTO_CHROMIUM_BUILD=false" \
              "PERFETTO_STANDALONE_BUILD=false" \
              "PERFETTO_START_DAEMONS=false" \
              "PERFETTO_IPC=false" \
              "PERFETTO_WATCHDOG=false" \
              "PERFETTO_COMPONENT_BUILD=false" \
              "PERFETTO_ENABLE_ETM_IMPORTER=false" \
              "PERFETTO_FORCE_DLOG_ON=false" \
              "PERFETTO_FORCE_DLOG_OFF=false" \
              "PERFETTO_FORCE_DCHECK_ON=false" \
              "PERFETTO_FORCE_DCHECK_OFF=false" \
              "PERFETTO_VERBOSE_LOGS=false" \
              "PERFETTO_VERSION_GEN=false" \
              "PERFETTO_TP_PERCENTILE=false" \
              "PERFETTO_TP_LINENOISE=false" \
              "PERFETTO_TP_HTTPD=false" \
              "PERFETTO_TP_JSON=false" \
              "PERFETTO_TP_INSTRUMENTS=false" \
              "PERFETTO_LOCAL_SYMBOLIZER=false" \
              "PERFETTO_ZLIB=true" \
              "PERFETTO_TRACED_PERF=false" \
              "PERFETTO_HEAPPROFD=false" \
              "PERFETTO_STDERR_CRASH_DUMP=false" \
              "PERFETTO_X64_CPU_OPT=false" \
              "PERFETTO_LLVM_DEMANGLE=false" \
              "PERFETTO_SYSTEM_CONSUMER=false" \
              "PERFETTO_THREAD_SAFETY_ANNOTATIONS=false" \
            )',
          ],
          'message': 'Generating build flags',
        },
      ],
    },
    {
      'target_name': 'protozero_plugin',
      'type': 'executable',
      'include_dirs': [
        '<(perfetto_root)/include',
        '<(perfetto_root)',
        '<(perfetto_gen_root)',
      ],
      'dependencies': [
        'perfetto_base',
        '<(protobuf_gyp_file):protoc_lib',
        '<(absl_gyp_file):abseil',
      ],
      'sources': [
        # deps/perfetto/src/protozero/protoc_plugin/BUILD.gn
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/protozero/protoc_plugin/BUILD.gn" "\\"protozero_plugin.*?sources = ")',
      ],
    },
    {
      'target_name': 'cppgen_plugin',
      'type': 'executable',
      'include_dirs': [
        '<(perfetto_root)/include',
        '<(perfetto_root)',
        '<(perfetto_gen_root)',
      ],
      'dependencies': [
        'perfetto_base',
        '<(protobuf_gyp_file):protoc_lib',
        '<(absl_gyp_file):abseil',
      ],
      'sources': [
        # deps/perfetto/src/protozero/protoc_plugin/BUILD.gn
        '<!@pymod_do_main(GN-scraper "<(perfetto_root)/src/protozero/protoc_plugin/BUILD.gn" "\\"cppgen_plugin.*?sources = ")',
      ],
    },
  ]
}
