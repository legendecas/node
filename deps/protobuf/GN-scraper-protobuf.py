import re
import os
import sys

PLAIN_SOURCE_RE = re.compile(r'\s*"([^/$].+)"\s*')
VARIABLE_RE = re.compile(r'\s*([_a-zA-Z]+)\s*=\s*"(?:\$([_a-zA-Z]+)/)?([^/$].+)"\s*')
PROTO_SOURCE_RE = re.compile(r'\s*"\$([_a-zA-Z]+)/([^/$].+)"\s*')
def DoMain(args):
  gn_filename, pattern = args
  src_root = os.path.dirname(gn_filename)
  with open(gn_filename, 'rb') as gn_file:
    gn_content = gn_file.read().decode('utf-8')

  matches = re.findall(VARIABLE_RE, gn_content)
  variables = {
    'root_out_dir': '',
  }
  for m in matches:
    val = m[2]
    if m[1] != '':
      val = f"{variables[m[1]]}/{val}"
    variables[m[0]] = val

  scraper_re = re.compile(pattern + r'\[([^\]]+)', re.DOTALL)
  matches = scraper_re.search(gn_content)
  match = matches.group(1)
  files = []
  for l in match.splitlines():
    m2 = PLAIN_SOURCE_RE.match(l)
    if m2:
      files.append(m2.group(1))
      continue
    m2 = PROTO_SOURCE_RE.match(l)
    if m2:
      files.append(f"{variables[m2.group(1)]}/{m2.group(2)}")
      continue
  # always use `/` since GYP will process paths further downstream
  rel_files = ['"%s/%s"' % (src_root, f) for f in files]
  return ' '.join(rel_files)

if __name__ == '__main__':
  print(DoMain(sys.argv[1:]))
