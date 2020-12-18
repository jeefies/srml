from . import tk
from . import config

class Login(tk.Frame):
    def __init__(self):
        super(Login, self).__init__(tk.root)
        self.pack()
        self.master.title('MailBox')
        self.master.geometry('200x200+200+200')

        self.check_auto_login()

        self.create_items()

    def run_main(self):
        pass

    def check_auto_login(self):
        log = config.mails.get('remember', '0')
        if log == '1':
            self.pack_forget()
            self.run_main()

    def create_items(self):
        ft = tk.Font(self, 'ft', size=10, weight=tk.ttf.BOLD)
        btnft = tk.Font(self, 'remember', size= 1)

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

        remember = tk.IntVar()
        chbtn = tk.Checkbutton(self, text='Remeber Me', variable = remember, font=btnft)
        chbtn.grid(row=7, column=0)
        self.rem = remember

        btn = tk.Button(self, command=self.prt, text='Submit')
        btn.grid(row=6, column=0)

    def prt(self, event = None):
        mail = self.mail.get()
        print('remember:', self.rem.get())
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
            config.pwd(pwd)
            mails['remember'] = str(self.rem.get())
            config.update()
            self.pack_forget()
            self.run_mail()
