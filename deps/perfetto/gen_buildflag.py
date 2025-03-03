import tempfile

def DoMain(args):
  fp = tempfile.NamedTemporaryFile('wt', delete=False)
  rsp_filepath = fp.name
  for arg in args:
    fp.write(arg)
    fp.write('\n')
  fp.close()

  return rsp_filepath
