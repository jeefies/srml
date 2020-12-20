import sys
import zlib
import base64
import os.path as opth
from configparser import ConfigParser

from .. import tk

__all__ = ('config', 'mails', 'sites', 'concats',
        'update', 'pwd', 'rpwd', '_login',
        'Concats', 'init', 'encrypt')

confn = 'config.conf' if sys.platform.startswith('li') \
        else 'config.ini' if sys.platform.startswith('win') or sys.platfrom.endswith('win') \
        else 'config.txt'

conf = opth.join(opth.dirname(opth.abspath(__file__)), confn)
config = ConfigParser()

def init():
    config.read(conf)
init()

def update():
    with open(conf, 'w') as f:
        config.write(f)


sections = ('mails', 'sites', 'concats')  # login info, login hosts and ports
for sec in sections:
    if not sec in config:
        config[sec] = {}

mails = config['mails']
sites = config['sites']
concats = config['concats'] # Concats

mailsavs = ('email', 'password', 'encrypt', 'remember')
sitesavs = ('pop_host', 'pop_port', 'smtp_host',
            'smtp_port',  'imap_host', 'imap_prot')

for i in mailsavs:
    if i not in mails:
        mails[i] = ''

for i in sitesavs:
    if i not in sites:
        sites[i] = ''
update()

def rpwd():
    return zlib.decompress(base64.b64decode(mails['password'])).decode() if mails['encrypt'] == 'true' else mails['password']

def pwd(pawd):
    mails['password'] = base64.b64encode(zlib.compress(pawd.encode())).decode()
    mails['encrypt'] = 'true'

def encrypt():
    if mails['encrypt'] != 'true':
        pwd(mails['password'])
    return 0

def _login():
    return (mails['email'], rpwd())

class _Concat:
    _ins = {}
    def __new__(self, name):
        if name not in self._ins:
            self._ins[name] = super().__new__(self)
        return self._ins[name]

    def __init__(self, name):
        self.name = name
        self.ccs = config['concats']
        self.var = tk.StringVar()
        self.update()

    @property
    def key(self):
        return self.name

    @property
    def val(self):
        return self.ccs[self.name]

    @key.setter
    def key(self, val):
        n = self.name
        old = self.val
        re = concats.pop(n)
        self.ccs[val] = old
        self._ins.pop(n)
        self._ins[val] = self
        self.name = val
        self.update()
        return re

    @val.setter
    def val(self, vall):
        self.ccs[self.name] = vall
        self.update()

    def update(self):
        self.var.set(str(self))

    def delete(self):
        self._ins.pop(self.name)
        self.ccs.pop(self.name)
        del self

    def __str__(self):
        return ' : '.join((self.key, self.val))

    def __repr__(self):
        return f"<concat {str(self)}>"

class Concats:
    def __init__(self):
        self.ccs = config['concats']

    @property
    def _names(self):
        return list(self.ccs)

    def place(self, index):
        return _Concat(self._names[index])
        
    def get(self, name):
        return _Concat(name)

    def gets(self, names):
        ccs = self.ccs
        return tuple(_Concat(name) for name in names)

    def __getitem__(self, index):
        return self.get(index)

    def __setitem__(self, index, val):
        self.ccs[index] = val

    def __iter__(self):
        self._i = 0
        self._vals = self.gets(self._names)
        return self

    def __next__(self):
        try:
            val = self._vals[self._i]
        except IndexError:
            raise StopIteration
        self._i += 1
        return val

    def __repr__(self):
        return f"<Concats for {len(self._names)}s>"
