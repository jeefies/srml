from . import tk
from . import config

class Login(tk.Frame):
    def __init__(self):
        super(Login, self).__init__(tk.root)
        self.pack()
        self.master.title('MailBox')
        self.master.geometry('200x200+200+200')

        self.create_items()

    def create_items(self):
        ft = tk.Font(self, size=10, weight=tk.ttf.BOLD, name='ft')

        tk.Label(self, text='Email', font='ft').grid(row=0, column=0)
        tk.Label(self, text='Password', font=ft).grid(row=2, column=0)
        tk.Label(self, text='Verify', font=ft).grid(row=4, column=0)

        mail = tk.StringVar()
        mail.set(config.mails['email'])
        mailen = tk.Entry(self)
        mailen['textvariable'] = mail
        mailen.grid(row=1, column=0)
        self.mail = mail
        # getitem, setitem

        pwd = tk.StringVar()
        pwden = tk.Entry(self, show='*')
        pwden['textvariable'] = pwd
        pwden.grid(row=3, column=0)
        self.pwd = pwd
        
        vpwd = tk.StringVar()
        vpwden = tk.Entry(self, show='*')
        vpwden['textvariable'] = vpwd
        vpwden.grid(row=5, column=0)
        self.vpwd = vpwd

        chbtn = tk.Checkbutton(self, text='Checkbtn')
        chbtn.grid(row=7, column=0)
        self.chbtn = chbtn

        btn = tk.Button(self, command=self.prt, text='Submit')
        btn.grid(row=6, column=0)

    def prt(self, event = None):
        mail = self.mail.get()
        print('btn:', self.chbtn.getboolean(self.chbtn))
        print('mail:', mail)
        pwd = self.pwd.get()
        vpwd = self.vpwd.get()
        if pwd != vpwd or pwd == '':
            tk.showwarning('PWD Error', 'Your password must be matched')
            self.pwd.set('')
            self.vpwd.set('')
        else:
            mails = config.mails
            mails['email'] = mail
            mails['password'] = pwd
            mails['encrypt'] = 0
            config.update()
            self.pack_forget()
