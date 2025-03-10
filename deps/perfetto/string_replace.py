import os
import sys
import pathlib

def DoMain(args):
  basedir, outdir, from_str, to_str = args[0:4]
  files = args[4:]

  output = []
  for file in files:
    relpath = os.path.dirname(os.path.relpath(file, basedir))
    filename = str(os.path.basename(file)).replace(from_str, to_str)
    output.append(os.path.join(outdir, relpath, filename))

  return ' '.join(output)
