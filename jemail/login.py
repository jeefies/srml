from srml import MailBox

from . import tk
from . import config

__all__ = ('Login',)

class Login(tk.Frame):
    def __init__(self, gls):
        self.gls = gls
        super(Login, self).__init__(tk.root)
        self.pack()
        self.master.title('MailBox')
        self.master.geometry('200x200+200+200')

        self.check_auto_login()

        self.create_items()

    def run_main(self):
        self.gls['Main'](self.gls)

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
        
        remember = tk.IntVar()
        chbtn = tk.Checkbutton(self, text='Remeber Me', variable = remember, font=btnft)
        chbtn.grid(row=7, column=0)
        self.rem = remember

        btn = tk.Button(self, command=self.prt, text='Submit')
        btn.grid(row=6, column=0)

    def prt(self, event = None):
        mail = self.mail.get()
        pwd = self.pwd.get()
        if mail == '':
            tk.showwarining('EMAIL Error', 'Your email is null')
        elif pwd == '':
            tk.showwarning('PWD Error', 'Your password is null')
        else:
            config.mails['remember'] = str(self.rem.get())
            config.update()
            mails = config.mails
            mails['password'] = pwd
            mails['encrypt'] = 'false'
            mails['email'] = mail
            self.pack_forget()
            self.run_main()
