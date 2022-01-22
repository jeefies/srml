import os
import sys
import time
import codecs
import smtplib
import logging

from email.utils import parseaddr, formatdate, formataddr, make_msgid
from email.header import Header

from markdown import markdown

from . import mime
from .msgbase import MSG

logger = logging


def sanitize_address(addr, encoding = "utf-8"):
    if isinstance(addr, str):
        addr = parseaddr(addr)

    nm, addr = addr
    nm = Header(nm, encoding).encode()
    return formataddr((nm, addr))

def sanitize_addresses(addresses, encoding = "utf-8"):
    return map(lambda x: sanitize_address(x, encoding), addresses)

def sanitize_subject(subject, encoding = "utf-8"):
    try:
        subject.encoding("ascii")
    except Exception:
        try:
            subject = Header(subject, encoding).encode()
        except Exception:
            subject = Header(subject, "utf-8").encode()

    return subject

def smtpconnect(smtp_host, mail, token_passwd, port = 465):
    try:
        logger.info("connecting to smtp")
        smtp = smtplib.SMTP_SSL(smtp_host, port)
        logger.info("Connecting with ssl succeeded")
    except Exception:
        smtp = smtp.SMTP(smtp_host, port)
        logger.info("Connection without ssl succeeded")
    logger.info("connet to %s with port %d", smtp_host, port)
    # smtp.connect(smtp.163.com, 465)
    # smtp.connect(smtp_host, port)
    smtp.ehlo()
    smtp.login(mail, token_passwd)
    return smtp

def easy_mail_sender(smtp_host, passwd, email, to_emails, subject, content, files_path = []):
    msg = mime.MIMEMultipart
    msg["From"] = email
    msg["To"] = ", ".join(sanitize_addresses(to_emails))
    msg["Subject"] = subject
    content = mine.MIMEText(content, plain, "utf-8")
    msg.attach(content)
    logger.info("add files if there's files")
    if files_path:
        for file in files_path:
            with codecs.open(file, "rb") as f:
                part = mime.MIMEApplication(f.read)
                part.add_header("Content-Disposition", "attachment", filename = os.path.basename(file))
                msg.attach(part)
                logger.info("add %s ok" % file)

    logger.info("sending...")
    smtp = smtpconnect(smtp_host, email, passwd)
    smtp.sendmail(email, to_emails, str(msg))
    smtp.close()
    logger.info("sending finish, \ncheck your email box to have a look")

def mdToHtml(file):
    try:
        with codecs.open(file, "r", "utf-8") as f:
            return markdown(f.read())
    except Exception:
        return None

def readFile(file):
    try:
        with codecs.open(file, "r", "utf-8") as f:
            return f.read()
    except Exception:
        return None

class Message(MSG):
    def __init__(self, subject = "",
            recipients  = [],
            body        = "",
            html        = "",
            mkd         = "",
            sender      = "",
            reply_to    = "",
            date        = None,
            files       = [],
            charset     ="utf-8"):
        "Class for an email message, noticed that the html or the mkd param must be string"
        self.sender = sender
        self.subject = subject
        self.recv = recipients
        self.body = body
        self.html = html
        self.mkd = mkd
        self.reply_to = reply_to
        self._date = date
        self.char = charset
        self.files = files
        self.msgID = make_msgid()

        logger.info("Message create")

    def __eq__(self, o):
        if not isinstance(o, Message):
            return super().__eq__(o)

        if (self.sender != o.sender):
            return False

        return (self.subject == o.subject and
                self.body == o.body and
                self.html == o.html and
                self.mkd == o.mkd and
                self._date == o._data)

    def _mimetext(self, text, subtype = "plain"):
        "Create MIMEText class with the given subtype"
        return mime.MIMEText(text, subtype, self.char)

    def as_string(self):
        return self._message.as_string()

    def as_bytes(self):
        return self._message.as_bytes()

    def __str__(self):
        return self.as_string()

    def __bytes__(self):
        return self.as_bytes()

    @property
    def _message(self):
        "Create the MIME Email"
        encode = self.char or "utf-8"
        if (len(self.files) == 0 and (not (self.html or self.mkd))):
            # If not files and only plain text
            msg = mime.MIMEMultipart()
            msg.attach(self._mimetext(self.body))
            print("text only")
        else:
            msg = mime.MIMEMultipart()
            alter = mime.MIMEMultipart("alternative")
            alter.attach(self._mimetext(self.body, "plain"))
            html = self.html + markdown(self.mkd)
            if html:
                alter.attach(self._mimetext(html, "html"))
                msg.attach(alter)

            print("with html, mkd: %s\n" % html)

        subject = sanitize_subject(self.subject, encode)
        print(subject)
        msg["Subject"] = subject
        msg["From"] = sanitize_address(self.sender, encode)
        print("from", msg["From"])
        msg["To"] = ", ".join(sanitize_addresses(self.recv))
        print("to", msg["To"])
        msg["Date"] = self.date
        print("Date", msg["Date"])
        msg["Message-ID"] = self.msgID
        print("Message-Id", self.msgID)

        # add reply context
        if self.reply_to:
            msg["Reply-To"] = sanitize_address(self.reply_to, encode)

        # add files
        for file in self.files:
            if not file:
                # ignore empty item
                continue

            if isinstance(file, str):
                with codecs.open(file, "rb") as f:
                    part = mime.MIMEApplication(f.read())
                    part.add_header("Content-Disposition", "attachment", filename=os.path.basename(file))
            else:
                part = mime.MIMEApplication(file[1])
                part.add_header("Content-Disposition", "attachment", filename=file[0])

            msg.attach(part)
    
        return msg

    @property
    def mail(self):
        if isinstance(self.sender, str):
            return self.sender
        return self.sender[1]

    @property
    def raw(self):
        return self.as_bytes()

    @property
    def date(self):
        return formatdate(self._date, localtime=1)

class Connect:
    def __init__(self, smtp_host, mails=None, smtp_port=465, ssl=True):
        if mails:
            self.mail, self.passwd = mails

        self.host = smtp_host
        self.port = smtp_port

        if ssl:
            try:
                self.smtp = smtplib.SMTP_SSL(smtp_host, smtp_port)
            except:
                ssl = False

        if not ssl:
            self.smtp = smtplib.SMTP(smtp_host, smtp_port)

    def login(self, mail, passwd):
        self.mail = mail
        self.passwd = passwd
        self.smtp.connect(self.host, self.port)
        self.smtp.ehlo()
        self.smtp.login(mail, passwd)

    def send(self, message):
        self.smtp.sendmail(message.mail, message.recv, str(message))

    def close(self):
        self.smtp.close()

    def __enter__(self):
        self.login(self.mail, self.passwd)
        return self

    def __exit__(self, exc_type, exc_val, tb):
        self.close()

    def to(self):
        return ", ".join(sanitize_addresses(self.recv))
