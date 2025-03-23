{
  "variables": {
    "jsoncpp_root": ".",
  },
  "targets": [
    {
      "target_name": "jsoncpp",
      "type": "static_library",
      "direct_dependent_settings": {
        "include_dirs": [
          "<(jsoncpp_root)/include",
        ],
      },
      "defines": [
        "JSON_USE_EXCEPTION=0",
        "JSON_USE_NULLREF=0",
      ],
      "include_dirs": [
        "<(jsoncpp_root)/include",
      ],
      "sources": [
        '<!@pymod_do_main(GN-scraper "<(jsoncpp_root)/BUILD.gn" "jsoncpp.*?sources = ")',
      ],
    }
  ]
}
