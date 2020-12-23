"""
This a easy package to send and recieve email with the terminal,
just in development, not support send too complex messages
"""
import sys
try:
    import click
except Exception as e:
    import logging
    logging.critical('You must installed click to use cli modules.')
    # sys.exit(1)
    del logging

import hy
from .sdml import easy_mail_sender, Message
from .sdml import Connect as SMTPConnect
from .popclient import POPClient as POPConnect
from .rcml import Connect as IMAPConnect
from .rcml import Parse, File
from .mailbox import MailBox
del hy
