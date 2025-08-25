#!/usr/bin/env python
# Copyright 2019 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from __future__ import print_function
import argparse
import sys
import os
import subprocess
import glob
import shutil


FILES_TO_SYNC = [
    'build_overrides/**',
    'gn/**',
    'include/**',
    'protos/**',
    'python/**',
    'src/**',
    'tools/**',

    'BUILD',
    'BUILD.extra',
    'BUILD.gn',
    'CHANGELOG',
    'README.md',
    'LICENSE',
    'pdl.py',
]

REVISION_LINE_PREFIX = 'Revision: '

def RunCmd(cmd):
  p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
  (stdoutdata, stderrdata) = p.communicate()
  if p.returncode != 0:
    raise Exception('%s: exit status %d', str(cmd), p.returncode)
  return stdoutdata.decode('utf-8')


def CheckRepoIsClean(path, suffix):
  os.chdir(path)  # As a side effect this also checks for existence of the dir.
  # If path isn't a git repo, this will throw and exception.
  # And if it is a git repo and 'git status' has anything interesting to say,
  # then it's not clean (uncommitted files etc.)
  if len(RunCmd(['git', 'status', '--porcelain'])) != 0:
    raise Exception('%s is not a clean git repo (run git status)' % path)
  if not path.endswith(suffix):
    raise Exception('%s does not end with /%s' % (path, suffix))


def CheckRepoIsNotAtMainBranch(path):
  os.chdir(path)
  stdout = RunCmd(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).strip()
  if stdout == 'main':
    raise Exception('%s is at main branch - refusing to copy there.' % path)


def CheckRepoIsPerfettoCheckout(path):
  os.chdir(path)
  revision = RunCmd(['git', 'config', '--get', 'remote.origin.url']).strip()
  if (revision != 'https://android.googlesource.com/platform/external/perfetto'):
    raise Exception('%s is not a proper perfetto checkout: %s' % (path, revision))


def FindFilesToSyncIn(path):
  files = []
  for f in FILES_TO_SYNC:
    files += [ file for file in glob.glob(os.path.join(path, f), recursive=True) if not os.path.isdir(file) ]
  files = [os.path.relpath(f, path) for f in files]
  return files


def FilesAreEqual(path1, path2):
  # We check for permissions (useful for executable scripts) and contents.
  return (os.stat(path1).st_mode == os.stat(path2).st_mode and
          open(path1, 'rb').read() == open(path2, 'rb').read())


def ReadV8IPRevision(node_src_path):
  lines = open(os.path.join(node_src_path, 'deps/v8/third_party/inspector_protocol/README.v8')).readlines()
  for line in lines:
    line = line.strip()
    if line.startswith(REVISION_LINE_PREFIX):
      return line[len(REVISION_LINE_PREFIX):]
  raise Exception('No V8 inspector protocol revision found')

def CheckoutRevision(path, revision):
  os.chdir(path)
  return RunCmd(['git', 'checkout', revision])


def GetHeadRevision(path):
  os.chdir(path)
  return RunCmd(['git', 'rev-parse', 'HEAD'])


def main(argv):
  parser = argparse.ArgumentParser(description=(
      "Rolls the perfetto project (upstream) into node's "
      "deps/perfetto (downstream)."))
  parser.add_argument("--upstream",
                      help="The perfetto (upstream) tree.",
                      default="~/perfetto")
  parser.add_argument("--node_src_downstream",
                      help="The nodejs/node src tree.",
                      default="~/nodejs/node")
  parser.add_argument('--force', dest='force', action='store_true',
                      help=("Whether to carry out the modifications "
                            "in the destination tree."))
  parser.set_defaults(force=False)

  args = parser.parse_args(argv)
  upstream = os.path.normpath(os.path.expanduser(args.upstream))
  downstream = os.path.normpath(os.path.expanduser(
      args.node_src_downstream))
  CheckRepoIsClean(upstream, '/perfetto')
  CheckRepoIsClean(downstream, '/node')
  CheckRepoIsPerfettoCheckout(upstream)
  # Check that the destination Git repo isn't at the main branch - it's
  # generally a bad idea to check into the main branch, so we catch this
  # common pilot error here early.
  CheckRepoIsNotAtMainBranch(downstream)

  src_dir = upstream
  dest_dir = os.path.join(downstream, 'deps/perfetto')
  print('Rolling %s into %s ...' % (src_dir, dest_dir))
  src_files = set(FindFilesToSyncIn(src_dir))
  dest_files = set(FindFilesToSyncIn(dest_dir))
  to_add = [f for f in src_files if f not in dest_files]
  to_delete = [f for f in dest_files if f not in src_files]
  to_copy = [f for f in src_files
             if (f in dest_files and not FilesAreEqual(
                 os.path.join(src_dir, f), os.path.join(dest_dir, f)))]
  print('To add: %s' % to_add)
  print('To delete: %s' % to_delete)
  print('To copy: %s' % to_copy)
  if not to_add and not to_delete and not to_copy:
    print('Nothing to do. You\'re good.')
    sys.exit(0)
  if not args.force:
    print('Rerun with --force if you wish the modifications to be done.')
    sys.exit(1)
  print('You said --force ... as you wish, modifying the destination.')
  for f in to_add + to_copy:
    os.makedirs(os.path.dirname(os.path.join(dest_dir, f)), exist_ok=True)
    contents = open(os.path.join(src_dir, f), 'rb').read()
    open(os.path.join(dest_dir, f), 'wb').write(contents)
    shutil.copymode(os.path.join(src_dir, f), os.path.join(dest_dir, f))
  for f in to_delete:
    os.unlink(os.path.join(dest_dir, f))
  head_revision = GetHeadRevision(upstream)
  lines = open(os.path.join(dest_dir, 'README.node')).readlines()
  f = open(os.path.join(dest_dir, 'README.node'), 'w')
  for line in lines:
    if line.startswith(REVISION_LINE_PREFIX):
      f.write(f'{REVISION_LINE_PREFIX}{head_revision}')
    else:
      f.write(line)
  f.close()


if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
