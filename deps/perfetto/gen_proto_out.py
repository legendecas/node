import os
import sys
import pathlib

def DoMain(args):
  basedir, outdir, suffix = args[0:3]
  proto_files = args[3:]

  output = []
  for file in proto_files:
    name, ext = os.path.splitext(os.path.basename(file))
    assert ext == '.proto'
    relpath = os.path.dirname(os.path.relpath(file, basedir))
    output.append(os.path.join(outdir, relpath, f'{name}.{suffix}.h'))
    output.append(os.path.join(outdir, relpath, f'{name}.{suffix}.cc'))

  return ' '.join(output)
