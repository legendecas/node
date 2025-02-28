#!/bin/sh
set -e
# Shell script to update protobuf in the source tree to the most recent version.
# Chrome's protobuf fork bumps version on the main branch and float their patches every
# time a new version is published in the upstream.

BASE_DIR=$(cd "$(dirname "$0")/../.." && pwd)
DEPS_DIR="$BASE_DIR/deps"

# shellcheck disable=SC1091
. "$BASE_DIR/tools/dep_updaters/utils.sh"

echo "Comparing latest upstream with current revision"

git fetch https://chromium.googlesource.com/chromium/src/third_party/protobuf.git HEAD

DIFF_TREE=$(git diff --diff-filter=d 'stash@{0}:deps/protobuf' FETCH_HEAD)

git stash drop

if [ -z "$DIFF_TREE" ]; then
  echo "Skipped because protobuf is on the latest version."
  exit 0
fi

# This is a rather arbitrary restriction. This script is assumed to run on
# Sunday, shortly after midnight UTC. This check thus prevents pulling in the
# most recent commits if any changes were made on Friday or Saturday (UTC).
# We don't want to pull in a commit that was just pushed, and instead rather
# wait for the next week's update. If no commits have been pushed in the last
# two days, we assume that the most recent commit is stable enough to be
# pulled in.
LAST_CHANGE_DATE=$(git log -1 --format=%ct FETCH_HEAD)
TWO_DAYS_AGO=$(date -d 'now - 2 days' '+%s')

if [ "$LAST_CHANGE_DATE" -gt "$TWO_DAYS_AGO" ]; then
  echo "Skipped because the latest version is too recent."
  exit 0
fi

LATEST_COMMIT=$(git rev-parse --short=7 FETCH_HEAD)

echo "Making temporary workspace..."

WORKSPACE=$(mktemp -d 2> /dev/null || mktemp -d -t 'tmp')

cd "$WORKSPACE"

mkdir protobuf

PROTOBUF_TARBALL="protobuf-v$NEW_VERSION.tar.gz"

echo "Fetching protobuf source archive"
curl -sL -o "$PROTOBUF_TARBALL" https://chromium.googlesource.com/chromium/src/+archive/refs/heads/main/third_party/protobuf.tar.gz

log_and_verify_sha256sum "protobuf" "$PROTOBUF_TARBALL"

gzip -dc "$PROTOBUF_TARBALL" | tar xf - -C protobuf/

rm "$PROTOBUF_TARBALL"

# Stash Node.js addition files
cp "$DEPS_DIR/protobuf/protobuf.gyp" "$DEPS_DIR/protobuf/GN-scraper.py" "$DEPS_DIR"

rm -rf "$DEPS_DIR/protobuf" protobuf/.git

# Restore Node.js modifications
mv protobuf "$DEPS_DIR/"

mv "$DEPS_DIR/protobuf.gyp" "$DEPS_DIR/GN-scraper.py" "$DEPS_DIR/protobuf/"

VERSION_NUMBER=$(grep "cpp" "$DEPS_DIR/protobuf/version.json" | sed -n "s/^.*cpp \"\(.*\)\"/\1/p")

NEW_VERSION="$VERSION_NUMBER-$LATEST_COMMIT"

# update version information in src/protobuf_version.h
cat > "$ROOT/src/protobuf_version.h" <<EOF
// This is an auto generated file, please do not edit.
// Refer to tools/dep_updaters/update-protobuf.sh
#ifndef SRC_PROTOBUF_VERSION_H_
#define SRC_PROTOBUF_VERSION_H_
#define PROTOBUF_VERSION "$NEW_VERSION"
#endif  // SRC_PROTOBUF_VERSION_H_
EOF

# Update the version number on maintaining-dependencies.md
# and print the new version as the last line of the script as we need
# to add it to $GITHUB_ENV variable
finalize_version_update "protobuf" "$NEW_VERSION" "src/protobuf_version.h"
