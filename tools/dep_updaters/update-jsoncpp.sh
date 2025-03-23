#!/bin/sh
set -e
# Shell script to update jsoncpp in the source tree to a specific version

BASE_DIR=$(cd "$(dirname "$0")/../.." && pwd)
DEPS_DIR="$BASE_DIR/deps"
[ -z "$NODE" ] && NODE="$BASE_DIR/out/Release/node"
[ -x "$NODE" ] || NODE=$(command -v node)

# shellcheck disable=SC1091
. "$BASE_DIR/tools/dep_updaters/utils.sh"

NEW_VERSION="$("$NODE" --input-type=module <<'EOF'
const res = await fetch('https://api.github.com/repos/open-source-parsers/jsoncpp/releases/latest',
  process.env.GITHUB_TOKEN && {
    headers: {
      "Authorization": `Bearer ${process.env.GITHUB_TOKEN}`
    },
  });
if (!res.ok) throw new Error(`FetchError: ${res.status} ${res.statusText}`, { cause: res });
const { tag_name } = await res.json();
console.log(tag_name.replace('v', ''));
EOF
)"

CURRENT_VERSION=$(grep "#define JSONCPP_VERSION_STRING" "$DEPS_DIR/jsoncpp/include/json/version.h" | sed -n "s/^.*VERSION \"\(.*\)\"/\1/p")

# This function exit with 0 if new version and current version are the same
compare_dependency_version "jsoncpp" "$NEW_VERSION" "$CURRENT_VERSION"

echo "Making temporary workspace..."

WORKSPACE=$(mktemp -d 2> /dev/null || mktemp -d -t 'tmp')

cleanup () {
  EXIT_CODE=$?
  [ -d "$WORKSPACE" ] && rm -rf "$WORKSPACE"
  exit $EXIT_CODE
}

trap cleanup INT TERM EXIT

JSONCPP_REF="v$NEW_VERSION"
JSONCPP_ZIP="jsoncpp-$JSONCPP_REF.zip"
JSONCPP_LICENSE="LICENSE-MIT"

cd "$WORKSPACE"

echo "Fetching jsoncpp source archive..."
curl -sL -o "$JSONCPP_ZIP" "https://github.com/open-source-parsers/jsoncpp/archive/refs/tags/$JSONCPP_REF.zip"
log_and_verify_sha256sum "jsoncpp" "$JSONCPP_ZIP"
unzip "$JSONCPP_ZIP"
rm "$JSONCPP_ZIP"

curl -sL -o "$JSONCPP_LICENSE" "https://raw.githubusercontent.com/open-source-parsers/jsoncpp/HEAD/LICENSE-MIT"

echo "Replacing existing jsoncpp (except GYP and GN build files)"
mv "$DEPS_DIR/jsoncpp/"*.gyp "$DEPS_DIR/jsoncpp/"*.gn "$DEPS_DIR/jsoncpp/"*.gni "$DEPS_DIR/jsoncpp/README.md" "$WORKSPACE/"
rm -rf "$DEPS_DIR/jsoncpp"
mv "$WORKSPACE" "$DEPS_DIR/jsoncpp"

# Update the version number on maintaining-dependencies.md
# and print the new version as the last line of the script as we need
# to add it to $GITHUB_ENV variable
finalize_version_update "jsoncpp" "$NEW_VERSION"
