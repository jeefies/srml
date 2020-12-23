import time
import poplib
from threading import Thread

POP_PORT = 110
POP_SSL_PORT = 995


class POPClient:
    "POP Client to use more easy with pop"

    def __init__(self, pophost, mails=None, popport=None, ssl=True):
        """
        pop host: The host name of the pop site to connect
        mails: a list or a tuple format in email, password
        pop port: The port of the connect
        ssl: Decide whether use ssl or not
        """
        if popport:
            self._pop = (pophost, popport)
            self.ssl = bool(ssl) if ssl else True
        else:
            if ssl:
                self.ssl = bool(ssl)
                self._pop = (pophost, POP_SSL_PORT)
            else:
                self.ssl = bool(1)
                self._pop = (pophost, POP_PORT)
        self.info = mails
        self.info = mails if mails else None

    def login(self, mail=None, passwd=None):
        ("login for the client, if mails and passwd doesn't \
given, use the info given when initialize")
        self.info = (mail, passwd) if mail else self.info
        info = self.info
        try:
            self.client.user(info[0])
            self.client.pass_(info[1])
        except:
            self.Client()
            self.login()
        self.list()

    def list(self):
        "return the message list, bigger number for later messgae"
        self._list = self._status(self.client.list())
        return self._list

    def Client(self):
        "initialize for the pop client"
        pop = poplib.POP3_SSL if self.ssl else poplib.POP3
        self.client = pop(*self._pop)
        return self.client

    def retr(self, num):
        "if the num is in the list, get the place in the list"
        if num in self._list:
            num = self._list.index(num) + 1
        return b'\n'.join(self._status(self.client.retr(num)))

    def _status(self, response):
        "The response of the return info"
        if b"OK" not in response[0]:
            raise RuntimeError('Not Avaliable')
        return response[1]
