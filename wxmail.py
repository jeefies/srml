from srml import MailBox
from srml.jpwd import pwd163, pwd126
try:
    import wx
except:
    import logging, sys
    logging.critical('Please download wxpython to use GUI mail subject')
    sys.exit(1)

import logging
logger = logging

EA = wx.EXPAND|wx.ALL

def Add(textctrl, content):
    textctrl.SetValue(textctrl.GetValue() + '{}\n'.format(content))
    return 1

class Login(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        self.Centre()

        self.panel = wx.Panel(self)
        panel = self.panel

        self.email = wx.TextCtrl(panel)
        self.passwd = wx.TextCtrl(panel)
        self.logbtn = wx.Button(panel, label='login')
        self.msg = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        self.logbtn.Bind(wx.EVT_BUTTON, self.createBox)

        box = wx.BoxSizer()

        # email ask
        emailbox = wx.BoxSizer(wx.VERTICAL)
        font = wx.Font(15, wx.FONTFAMILY_SCRIPT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_LIGHT)
        _em = wx.StaticText(panel, wx.ALIGN_LEFT, label='Email Address')
        _em.SetFont(font)
        emailbox.Add(_em, proportion=1, flag=EA, border=3)
        emailbox.Add(self.email, proportion=1, flag=EA, border=3)
        box.Add(emailbox, proportion=2, flag=EA, border=5)
        
        # password ask
        pwdbox = wx.BoxSizer(wx.VERTICAL)
        _pw = wx.StaticText(panel, wx.ALIGN_LEFT, label='Login Password')
        _pw.SetFont(font)
        pwdbox.Add(_pw, proportion=1, flag=EA, border=3)
        pwdbox.Add(self.passwd, proportion=1, flag=EA, border=3)
        box.Add(pwdbox, proportion=2, flag=EA, border=5)
        
        # submit and change GUI
        subbox = wx.BoxSizer(wx.VERTICAL)
        subbox.Add(self.logbtn, proportion=1, flag=EA, border=3)
        redi = wx.Button(self.panel, label='Redirect')
        subbox.Add(redi, proportion=1, flag=EA, border=3)
        redi.Bind(wx.EVT_BUTTON, self.des)
        #redi.Hide()
        self.redi = redi
        box.Add(subbox, proportion=1, flag=EA, border=3)

        # show message.
        self.box = wx.BoxSizer(wx.VERTICAL)
        self.box.Add(box, proportion=2, flag=EA, border=5)
        self.box.Add(self.msg, proportion=5, flag=EA, border=5)

        panel.SetSizer(self.box)

    def createBox(self, event):
        mail = self.email.GetValue()
        pwd = self.passwd.GetValue()

        # self password to test
        if pwd == 'pwd163':
            pwd = pwd163
        if pwd == 'pwd126':
            pwd = pwd126
        
        # both mail and password is enter
        if mail and pwd:
            Add(self.msg, "Try to login now, it might take a few seconds.") # Show start login info
            logger.info('login email, email={}, pwd={}'.format(mail, pwd))

            if hasattr(self, 'mlbox'): # check if logined
                Add(self.msg, "Login changed.")
            self.mlbox = MailBox(None, (mail, pwd))
            try:
                logger.info('login box')
                self.mlbox.login() # Start login
                Add(self.msg, 'Login success')
            except:
                logger.warn('login failed') # Fail login and show failed error
                Add(self.msg ,'Error email or password.\nNotice the password is for \n\tlogining for the smtp, imap, pop')
                return 0
        else: # The mail and password is not enter
            Add(self.msg, 'Please enter your email and passwd')
            return 0
        Add(self.msg, "Type the  redirect button to get to the using frame.") # add redirect button.
        self.redi.Show()
        return 1

    def des(self, event):
        if not hasattr(self, 'mlbox'):
            Add(self.msg, 'Please login first.')
            return 0
        if not self.mlbox.logined:
            Add(self.msg, 'Please login again.')
            return 0
        self.Destroy()
        boxinstance = Box(self.mlbox)
        boxinstance.Show()
        return 1

class Box(wx.Frame):
    def __init__(self, box):
        wx.Frame.__init__(self, None, title='Mail Box', size=(1000, 800))
        self.box = box
        self.Centre()
        self.CreateStatusBar()
        self.SetStatusText('Login for {}'.format(self.box.mails[0]))
        self.makeMuneBar()

    def makeMuneBar(self):
        fileMenu = wx.Menu()


if __name__ == '__main__':
    app = wx.App()
    frame = Login(None, title='Mail Box', size=(600, 400))
    frame.Show()
    frame.Centre()
    app.MainLoop()
