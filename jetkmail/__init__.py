"""
A GUI of MailBox,
Author: Jeef
Email: jeefy163@163.com
# if you want my qq or wechat, please email me
"""
"""
A package depends on tkinter to use MailBox in a easy way
Documents for
[1]: docs.python.org/3/library/tkinter.html
[2]: coderslegacy.com/python/python-gui
[3]: blog.csdn.com

Url: https://github.com/jeefies/srml
You can see it on github, also on pypi.
"""

from .login import Login
from .tk import root

def _main():
    log = Login()
    root.mainloop()
