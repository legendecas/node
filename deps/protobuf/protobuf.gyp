{
  'variables': {
    'PROTOBUF_ROOT': './',
    'absl_gyp_file': '../../tools/v8_gypfiles/abseil.gyp',
    'GN-scraper': 'GN-scraper-protobuf',
  },
  'targets': [
    {
      'target_name': 'protobuf_lite',
      'type': 'static_library',
      'toolsets': ['host', 'target'],
      'include_dirs': [
        'src',
      ],
      'direct_dependent_settings': {
        'include_dirs': [
          '<(PROTOBUF_ROOT)/src',
        ],
      },
      'sources': [
        '<!@pymod_do_main(<(GN-scraper) "<(PROTOBUF_ROOT)/proto_sources.gni" "protobuf_lite_sources = ")',
        '<!@pymod_do_main(<(GN-scraper) "<(PROTOBUF_ROOT)/proto_sources.gni" "protobuf_headers = ")',
      ],
      'dependencies': [
        'utf8_range',
        '<(absl_gyp_file):abseil',
      ],
    },
    {
      'target_name': 'protobuf_full',
      'type': 'static_library',
      'include_dirs': [
        'src',
      ],
      'direct_dependent_settings': {
        'include_dirs': [
          '<(PROTOBUF_ROOT)/src',
        ],
      },
      'sources': [
        '<!@pymod_do_main(<(GN-scraper) "<(PROTOBUF_ROOT)/proto_sources.gni" "protobuf_lite_sources = ")',
        '<!@pymod_do_main(<(GN-scraper) "<(PROTOBUF_ROOT)/proto_sources.gni" "protobuf_sources = ")',
        '<!@pymod_do_main(<(GN-scraper) "<(PROTOBUF_ROOT)/proto_sources.gni" "protobuf_headers = ")',
      ],
      'dependencies': [
        'utf8_range',
        '<(absl_gyp_file):abseil',
      ],
    },
    {
      'target_name': 'protoc_lib',
      'type': 'static_library',
      'include_dirs': [
        '<(PROTOBUF_ROOT)/src',
      ],
      'direct_dependent_settings': {
        'include_dirs': [
          '<(PROTOBUF_ROOT)/src',
        ],
      },
      'sources': [
        '<!@pymod_do_main(GN-scraper-protobuf "<(PROTOBUF_ROOT)/proto_sources.gni" "protoc_sources = ")',
        '<!@pymod_do_main(GN-scraper-protobuf "<(PROTOBUF_ROOT)/proto_sources.gni" "protoc_headers = ")',
      ],
      'dependencies': [
        'protobuf_full',
        '<(absl_gyp_file):abseil',
      ],
    },
    {
      'target_name': 'protoc',
      'type': 'executable',
      'toolsets': ['host'],
      'include_dirs': [
        'src',
      ],
      'sources': [
        '<!@pymod_do_main(<(GN-scraper) "<(PROTOBUF_ROOT)/proto_sources.gni" "protoc_cpp_sources = ")',
        '<!@pymod_do_main(<(GN-scraper) "<(PROTOBUF_ROOT)/proto_sources.gni" "protoc_cpp_headers = ")',
        '<!@pymod_do_main(<(GN-scraper) "<(PROTOBUF_ROOT)/proto_sources.gni" "protoc_python_sources = ")',
        '<!@pymod_do_main(<(GN-scraper) "<(PROTOBUF_ROOT)/proto_sources.gni" "protoc_python_headers = ")',
        '<!@pymod_do_main(<(GN-scraper) "<(PROTOBUF_ROOT)/BUILD.gn" "\\"protoc\\".*?sources = ")',
      ],
      'dependencies': [
        'protobuf_full',
        'protoc_lib',
        '<(absl_gyp_file):abseil',
      ],
    },
    {
      'target_name': 'utf8_range',
      'type': 'static_library',
      'include_dirs': [
        'third_party/utf8_range',
      ],
      'direct_dependent_settings': {
        'include_dirs': [
          'third_party/utf8_range',
        ],
      },
      'sources': [
        '<!@pymod_do_main(<(GN-scraper) "<(PROTOBUF_ROOT)/BUILD.gn" "\\"utf8_range\\".*?sources = ")',
      ],
      'dependencies': [
        '<(absl_gyp_file):abseil',
      ],
    },
  ]
}