import os

def DoMain(args):
  basedir, = args[0:1]
  files = args[1:]

  output = []
  for file in files:
    output.append(os.path.relpath(file, basedir))

  return ' '.join(output)
