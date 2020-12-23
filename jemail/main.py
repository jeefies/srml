import os
from threading import Thread
from srml import MailBox
from srml.mailbox import AuthenticationError

from . import tk, config


__all__ = ('Main',)

class Main(tk.Frame):
    def __init__(self, gls):
        super().__init__(tk.root)
        self.gls = gls
        root = tk.root
        mw, mh = root.maxsize()
        root.geometry(f'{mw // 2}x{mh // 2}+{mw // 4}+{mh // 4}')

        self.create_menu()

        self.pack()
        self.login()

        self.sbind()

    def sbind(self):
        self.master.bind("<Control-n>", self.new)
        self.bind_all("<Control-t>", self.concats)
        
    def create_menu(self):
        mainmenu = tk.Menu(self)
        
        # menu Email
        filemn = tk.Menu(mainmenu, tearoff=0)
        af = filemn.add_command
        filemn.add_command(label = 'Open', command = self.askopen)
        filemn.add_command(label = 'Save', command = self.save)
        af(label='New', command = self.new)
        filemn.add_separator()
        filemn.add_command(label = 'Exit', command = self.exit)
        mainmenu.add_cascade(label = 'File', menu=filemn)

        # menu email
        mailmn = tk.Menu(mainmenu, tearoff=0)
        am = mailmn.add_command
        am(label = 'Sended', command = self.sended)
        am(label = 'Received', command = self.recved)
        mainmenu.add_cascade(label = "Email", menu = mailmn)

        # menu config
        configmn = tk.Menu(mainmenu, tearoff=0)
        configmn.add_command(label = 'User', command = self.modify_con)
        configmn.add_command(label = 'Concat', command = self.concats)
        mainmenu.add_cascade(label = 'Config', menu=configmn)

        # menu help
        helpmn = tk.Menu(mainmenu, tearoff=0)
        helpmn.add_command(label = "Usage", command = self.usage)
        helpmn.add_command(label = "About", command = self.about)
        mainmenu.add_cascade(label = "Help", menu = helpmn)

        tk.root.config(menu = mainmenu)
        
    def usage(self):
        pass

    def about(self):
        pass

    def new(self, event = None):
       self.gls['Writer'](self.gls, self.box)

    def sended(self):
        pass

    def concats(self, event=None):
        self.gls['ConcatConfig'](self.gls)

    def recved(self):
        pass

    def modify_con(self):
        self.gls['UserConfig'](self.gls)
        self.login()
        
    def askopen(self):
        fts = (('JE mail file', '.Jml'), ('TXT File', '.txt'), ('ALL File', '*'))
        file = tk.askopenfilename(parent=self, title='jemail', \
                initialdir=os.getcwd(), filetypes=fts)
        print(file)
        
    def exit(self):
        self.pack_forget()
        #self.master.desteroy()
        
    def save(self):
        pass

    def login(self):
        self.box = MailBox(mails = config._login())
        def _login():
            try:
                self.box.login()
                print('login success')
                config.encrypt()
                config.update()
            except AuthenticationError:
                tk.showwarning('PWD Error', 'Not the right password, please use imap/smtp/pop password.')
                config.mails['remember'] = '0'
                self.exit()
                self.gls['Login'](self.gls)
        thr = Thread(target = _login)
        thr.setDaemon(True)
        thr.start()
