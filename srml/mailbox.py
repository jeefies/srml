"""
A module to define the class named MailBox
MailBox is a class to send and recieve the email messages.
"""
import time
from . import Message, SMTPConnect, IMAPConnect, POPConnect, Parse
from smtplib import SMTPAuthenticationError


class MailBox:
    """
    A class for mail sending and recieving.
    Message is create by MIME.
    Use smtp to send mails, use pop and imap to recieve or manage the emails.
    Make sure that your email account can be used for them.
    """

    def __init__(self, host=None, mails=None, ssl=True):
        """
        Recieve the host and the email info arguments.
        Host is the host of the imap, smtp and the pop site.
        If a host like `some.com` is given, the hosts would automatic complete
        like `smtp.some.com`, `imap.some.com`, `pop.some.com`.
        But only the email address is given such as `name@example.com`,
        The hosts also would automatic complete like
        `smtp.example.com`, `imap.example.com`, `pop.example.com`.
        Argument mails is a list or a tuple like
            ('myemail@some.com', 'MYPASSWORD').
        However, the password is not the password for the account \
but for logining for the protocal.
        Vistsing the email site to open for the protocal.
        Notice, if you want to change one of the protocol's host, \
you can set like this:
            box = MailBox('163.com')
            # also box = MailBox(mails=('myaccount@163com', 'MYPASSWORD'))
            # if host is not given but mails does, \
MailBox would autoanalyze the host of the mail
            # However, you can change the hosts by yourself if you want
            box.hosts['pop'] = 'pop.qq.com'
            box.hosts['imap'] = 'imap.gmail.com'
            box.host = '126.com' # Change the whole hosts
        If you don't want to use the default port of the site, \
you can set like this:
            box.ports['smtp'] = 465
        argument ssl decide use ssl to connect or not.
        Here is an example usage:
            box = MailBox('163.com', ('example@163.com', 'MYPASSWORD'))
            # create the instance for the mailbox
            box.login() # login the account, connect to the host
            msg = box.createMessage('name')
            # Do not create more then one message at once.
            # the only argument is for the name to send
            msg.subject = "Subject"
            msg.body = 'This is the body part, if the html or \
mkd is given, this would be shown'
            msg.html = "<h1>HTML CONTENT TITLE</h1>"
            # Advice: that it's better not to use html \
to modify the content of the message
            msg.mkd = "*markdown italic*, and __BOLD__"
            msg.recv = \
['receive_email@some.com', 'another_receive@anaother.com']
            msg.sender = 'youraccount@your.net'
            #if you were logined, this step is not neccasary
            box.send(msg) #send the message after login
            #box.update() # if the connect time is out, connect fresh again
        """
        self.anahost(host, mails)
        self.ssl = ssl
        self.ports = {'smtp': (465 if ssl else 25), 'pop': (
            995 if ssl else 110), 'imap': (993 if ssl else 143)}
        self._logined = 0

        def __Noop(self):
            while 1:
                while self._logined:
                    self.smtp.noop()
                    self.pop.noop()
                    self.imap.noop()

    def anahost(self, host, mails):
        "the function to analyze the host of the mail"
        self.hosts = {'smtp': None, 'pop': None, 'imap': None}

        if mails:
            mail = mails[0]
            pwd = mails[1]
            self.mails = mails[:2]
        else:
            mail = None

        if mail:
            ends = mail.split('@')[-1] if not host else host
        else:
            ends = None

        if ends:
            for pre in self.hosts:
                self.hosts[pre] = '{0}.{1}'.format(pre, ends)

    def login(self, mail=None, passwd=None):
        "Login for the mailbox"
        "if mail and passwd is not given,"
        "it would use the info given when creating the mailbox"
        if mail and passwd:
            self.mails = (mail, passwd)
        mails = self.mails
        self.smtp = SMTPConnect(
            self.hosts['smtp'], self.mails, self.ports['smtp'], self.ssl)
        self.pop = POPConnect(
            self.hosts['pop'], self.mails, self.ports['pop'], self.ssl)
        self.imap = IMAPConnect(
            self.hosts['imap'], self.mails, self.ports['imap'], self.ssl)
        for pro in (self.smtp, self.pop, self.imap):
            try:
                pro.login(*mails)
            except SMTPAuthenticationError:
                raise AuthenticationError('Failed to login, ask author at jeefy163@163.com for help')
        self._logined = 1

    @property
    def logined(self):
        return bool(self._logined)

    def createMessage(self, name=None):
        self.msg = Message()
        sender = (name, self.mails[0]) if name else self.mails[0]
        # print(sender)
        self.msg.sender = sender
        self.msg.date = time.time()  # time.strftime('%a, %d %b %Y %H:%M:%s')
        return self.msg

    def recentReceive(self):
        pop = self.pop
        last = len(pop.list())
        msg = Parse(pop.retr(last))
        return msg

    def recentSend(self):
        if hasattr(self, 'msg'):
            return self.msg
        self.imap.client.id_({'name': 'IMAPClient', 'version': '2.1.0'})
        self.imap.select_folder('已发送')
        self._sduids = uids = self.imap.search('ALL')
        bmsg = self.imap.fetch(uids[-1])[b'BODY[]']
        self.imap.client.close_folder()
        return Parse(bmsg)

    def allReceive(self):
        for uid in self.pop.list():
            par = Parse(self.pop.retr(uid))
            yield (par.dict()['Subject'], par)

    def allSend(self):
        self.imap.client.id_({'name': 'IMAPClient', 'version': '2.1.0'})
        self.imap.select_folder('已发送')
        if not hasattr(self, '_sduids'):
            self._sduids = self.imap.search('ALL')
        for uid in self._sduids:
            bmsg = self.imap.fetch(uid)[b'BODY[]']
            par = Parse(bmsg)
            yield (par.dict()['Subject'], par)

    def send(self, msg):
        return self.smtp.send(msg)

    def update(self):
        self.login()

class AuthenticationError(Exception): pass
