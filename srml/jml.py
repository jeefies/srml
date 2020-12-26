import io
import bz2
import json
import base64
import codecs

from . import Parse, Message, File


class Smessage(Message):
    def to_json(self, fn = None, fp=None):
        di = self.jdict()
        if fp:
            f = fp
        elif not fn:
            f = io.StringIO()
        else:
            f = codecs.open(fn)
        json.dump(di, f, indent = 4)
        return f

    def dict(self):
        di = {'From': self.sender,
            'Subject': self.subject,
            'To': self.to(),
            'Body': self.body,
            'Html': self.html,
            'Mkd': self.mkd,
            'Reply-To': self.reply_to,
            'Date': self._date,
            'Char': self.char,
            'Files': [File(f) for f in self.files],
            'Message-ID': self.msgID
                }
        return di

    def jdict(self):
        di = self.dict()
        di['Files'] = [File(f).info() for f in self.files]
        return di

    @staticmethod
    def from_json(fn):
        d = json.load(codecs.open(fn))
        self = Smessage()
        self.sender = tuple(d['From'])
        self.subject = d['Subject']
        self.recv = [r for r in map(lambda x: x.strip(), d['To'].split(', ')) if r]
        self.body = d['Body']
        self.html = d['Html']
        self.mkd = d['Mkd']
        self.reply_to = d['Reply-To']
        self._date = d['Date']
        self.char = d['Char']
        self.files = [File().from_info(info) for info in d['Files']]
        self.msgID = d['Message-ID']
        return self

    def __eq__(self, o):
        if isinstance(o, Smessage):
            return self.dict() == o.dict()
        else:
            return super().__eq__(o)
