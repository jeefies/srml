import os
from time import strftime
from srml import MailBox, Parse, File, Message

box = MailBox(mails = (os.getenv('MAIL_TEST'), os.getenv('MAIL_PWD')))

def test_init():
    hosts = box.hosts
    assert hosts['pop'] == 'pop.126.com'
    assert hosts['imap'] == 'imap.126.com'

    box.login()

def test_crmsg():
    global msg
    msg = box.createMessage('MyM-Box')
    msg.subject = 'TEST'
    msg.body = """
Hi, I'm testing the MailBox, if it's not Jeefy there, please don't use the test models
    """
    msg.mkd = """# Test
*Notice*: you're testing the mailbox at {}.  
If is not the test to your self, please close the program to avoid disturbing.  
## Thank you
    """.format(strftime('%Y.%m.%d %H:%M'))
    msg.recv = [os.getenv('MAIL_TEST')]

def test_rec():
    rcmsg = box.recentReceive()
    # print(rcmsg)

def testsend():
    rcsend = box.recentSend()
    assert rcsend == msg
    box.send(msg)

def test_update():
    box.update()

def test_alls():
    for msg in box.allSend():
        # print(msg)
        pass

def test_allr():
    for msg in box.allReceive():
        # print(msg)
        pass

if __name__ == "__main__":
    test_init()
    test_crmsg()
    test_rec()
    testsend()
    test_update()
    test_alls()
    test_allr()

