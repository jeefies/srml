import sys
import os.path as opth
from configparser import ConfigParser

__all__ = ('config', 'mails', 'sites', 'concats', 'update')

confn = 'config.conf' if sys.platform.startswith('li') \
        else 'config.ini' if sys.platform.startswith('win') or sys.platfrom.endswith('win') \
        else 'config.txt'

conf = opth.join(opth.dirname(opth.abspath(__file__)), confn)
config = ConfigParser()

config.read(conf)


def update():
    with open(conf, 'w') as f:
        config.write(f)


sections = ('mails', 'sites', 'concats')  # login info, login hosts and ports
for sec in sections:
    if not sec in config:
        config[sec] = {}

mails = config['mails']
sites = config['sites']
concats = config['concats']

mailsavs = ('email', 'password', 'encrypt')
sitesavs = ('pop_host', 'pop_port', 'smtp_host',
            'smtp_port',  'imap_host', 'imap_prot')

for i in mailsavs:
    if i not in mails:
        mails[i] = ''

for i in sitesavs:
    if i not in sites:
        sites[i] = ''
update()
