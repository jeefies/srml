import os
import time
import codecs
import email
from threading import Thread

from imapclient import IMAPClient
import hy as __hy
from .msgbase import MSG


class Connect:
    "Connect with IMAPClient"

    def __init__(self, imap=None, email=None, port=None, ssl=True):
        """
        :param imap is a string for imap host name to connect
        :param email is a tuple of the email's info
            format in email, password
        :param port for the port of the imap host to connect
        """
        self.imapinfo = (imap, port)
        self.mail, self.passwd = email if email else (None, None)
        self.folder = 'INBOX'
        self.ssl = ssl

    def _noopthr(self):
        def _innernoop():
            while True:
                time.sleep(2)
                self.noop()
        thr = Thread(target = _innernoop)
        thr.setDaemon(True)
        thr.start()

    def _noop(self):
        self.client.noop()

    def Client(self, imap=None, ssl=True, **kwargs):
        "Create and return IMAPClient instance, param imap is format in imap-host, imap-port, others for IMAPClient kwargs"
        try:
            ssl = ssl if ssl else self.ssl
            imap = imap if imap else self.imapinfo
            self.cli = IMAPClient(*imap, ssl=ssl, **kwargs)
            return self.cli
        except Exception as e:
            return "ERROR >>" + str(e)

    @property
    def client(self):
        if hasattr(self, 'cli'):
            return self.cli
        return self.Client()

    def login(self, mail=None, passwd=None):
        "Login the imapclient, if not give there, use the info given when initialize. Return the login result"
        # give the id so can login to imap.163.com
        try:
            self.client.id_({'name':'IMAPClient', 'version': '2.1.0'})
        except:
            self.Client()
        user = (mail, passwd) if (mail and passwd) else (
            self.mail, self.passwd)
        return self.client.login(*user)

    def list_folders(self):
        "return all folder's status and name"
        return self.client

    def close_folder(self):
        "close the currently select folder"
        return self.client.close_folder()

    def select_folder(self, folder='INBOX'):
        "Default select INBOX folder, if folder is given, select the given folder"
        self.folder = folder if folder else self.folder
        return self.client.select_folder(self.folder)

    def search(self, types='ALL'):
        "search for all the contents if the types is not given, types can be a string or a tuple or a list"
        return self.client.search(types)

    def fetch(self, uid, types=["BODY[]"]):
        "fetch for body of the uid if the types isn't given or according to the types, return the fetch result"
        return self.client.fetch(uid, types)[uid]

    def fetchall(self, types=['BODY[]']):
        "return all of the content according to the types, default 'BODY[]'. By a generation"
        for uid in self.search():
            yield self.fetch(uid)

    def quit(self):
        "exit the client"
        self.client.logout()
        # self.client.shutdown()

    def __enter__(self):
        self.client()
        self.login()
        return self

    def __exit__(self, exc_type, exc_val, tb):
        self.quit()


class Parse(MSG):
    def __init__(self, from_bytes):
        "Read from the bytes"
        self.msg = email.message_from_bytes(from_bytes)
        self._con = []
        self.raw = self.msg.as_bytes()

    def decode(self, con):
        head = email.header.Header(con)
        res = email.header.decode_header(str(head))[0]
        con = res[0] #.decode(res[0][1])
        try:
            return con.decode(res[1])
        except:
            return con

    @staticmethod
    def _bs(bos):
        "bytes to string"
        try:
            return bos.decode('utf-8')
        except:
            return bos

    @classmethod
    def _mc(cls,msg):
        "decode msg's content"
        return cls._bs(msg.get_payload(decode=1))

    def __getattr__(self, attr):
        try:
            return self.__dict__[attr]
        except KeyError:
            return self.msg.get(attr, None)

    def get_con(self, msg=None):
        "get all content of the parts"
        if msg is None:
            msg = self.msg
            self._con = []
        if msg.is_multipart():
            s = self._con
            walk = msg.walk()
            next(walk)
            for imsg in walk:
                s.append(self.get_con(imsg))
        else:
            return self._mc(msg)
    @property
    def body(self):
        msg = self.msg
        if not msg.is_multipart():
            return self._mc(msg)
        main = tuple(msg.walk())[1]
        def get_main_body(msg):
            if msg.is_multipart():
                return get_main_body(tuple(msg.walk())[-1])
            return self._mc(msg)
        return get_main_body(main)

    @property
    def text(self):
        msg = self.msg
        if not msg.is_multipart():
            return self._mc(msg)
        main = tuple(msg.walk())[1]
        def get_main_text(msg):
            if msg.is_multipart():
                return get_main_text(tuple(msg.walk())[1])
            return self._mc(msg)
        return get_main_text(main)

    #@property
    def dict(self):
        "Return a dict of almost all info"
        s = {}
        for attr in ['From', 'To', 'Cc', 'Subject']:
            s[attr] = self.decode(getattr(self, attr))
        s['param'] = self.get_param()
        return s

    def get_param(self, msg=None):
        "get Files"
        if msg is None:
            msg = self.msg
        if msg.is_multipart():
            tup = msg.walk()
            s = []
            next(tup)
            for imsg in tup:
                appd = tuple(self.get_param(imsg))
                if appd:
                    s.append(appd)
            return s
        else:
            s = []
            msgtype = msg['Content-Type']
            if 'application' in msgtype:
                filename = msg['Content-Disposition'].split('"')[-2]
                body = msg.get_payload()
                appd = File(filename, body)
                s.append(appd)
            name = msg.get_param('name')
            if name:
                s.append(File(name, msg.get_payload()))
            return s

    def __str__(self):
        return self.text + '\n\r\n\r' + self.body


class File:
    "File class to save and read single file"
    __slots__ = ['name', 'encode', 'con', 'error']
    def __init__(self, name, con='', encode=None):
        "init the file with the name and the con"
        self.name = os.path.abspath(str(name))
        self.encode = encode
        self.con = con
        self.error = 0

    def __repr__(self):
        return "<File {}>".format(self.name)

    def write(self):
        "write the content in the file for normal mod"
        with codecs.open(self.name, 'w', self.encode) as f:
            try:
                f.write(self.con)
                self.error = 0
            except Exception as e:
                self.error += 1
                if self.error > 3:
                    raise e
                self.bwrite()

    def bwrite(self):
        "write the content in binary mod"
        with codecs.open(self.name, 'wb') as f:
            try:
                f.write(self.con)
                self.error = 0
            except Exception as e:
                self.error += 1
                if self.error > 3:
                    raise e
                self.write(self.con)

    def read(self):
        "Read the file in normal mode"
        self.con = codecs.open(self.name, 'r', self.encode).read()
        return self.con

    def bread(self):
        "Read the file in binary mode"
        self.con = codecs.open(self.name, 'rb').read()
        return self.con
