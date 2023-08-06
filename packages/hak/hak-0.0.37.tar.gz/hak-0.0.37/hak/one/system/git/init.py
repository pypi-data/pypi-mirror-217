from subprocess import run as sprun
from hak.one.directory.make import f as mkdir
from hak.one.directory.remove import f as rmdir
_root = '../temp_git_init'

def up(): mkdir(_root)

def dn(): rmdir(_root)
args = ['git', 'init']

f = lambda cwd: sprun(cwd=cwd, capture_output=True, args=args)

def t():
  up()
  z = f(_root)
  dn()
  return all([
    z.args==args,
    z.returncode==0,
    'Initialized empty Git repository in' in z.stdout.decode('utf-8'),
    not z.stderr.decode('utf-8')
  ])
