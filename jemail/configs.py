from . import tk
from .config import mails, rpwd
from . import config


def UserConfig(gls):
    chd = tk.Toplevel()
    mh, mw = chd.maxsize()
    chd.geometry(f'320x200+{round(mh/3.5)}+{round(mw//3.5)}')
    _UserConfig(chd, gls).pack()
    chd.mainloop()

class _UserConfig(tk.Frame):
    def __init__(self, master, gls):
        super().__init__(master)
        self.gls = gls
        self.crt_item()

    def crt_item(self):
        # Email label
        tk.Label(self, text='Email:').grid(row=0, column=0)

        # Email Entry
        email = tk.StringVar()
        email.set(mails['email'])
        en = tk.Entry(self, width = 25)
        en['textvariable'] = email
        en.grid(row=0, column=1)
        self.email = email
    
        tk.Label(self).grid(row=1)

        # Password label
        tk.Label(self, text='Password:').grid(row=2, column=0)

        # pwd entry
        pwd = tk.StringVar()
        pwd.set(rpwd())
        pwden = tk.Entry(self, cnf={'textvariable': pwd}, show='*', width=25)
        pwden.grid(row=2, column = 1)
        self.pwd = pwd

        #tk.Label(self).grid(row=3)
        
        # show pwd
        def change():
            pwden['show'] = str() if pwden['show'] else '*'
        tk.Button(self, text='Show pwd', command = change).grid(row=4)

        tk.Label(self).grid(row=5)

        # submit
        btn = tk.Button(self, text = 'Submit', command=self.submit)
        btn.grid(row=6, column=0)

        # remember
        rem = tk.IntVar()
        cb = tk.Checkbutton(self, text='remember', variable=rem)
        cb.grid(row=6, column=1)
        nou = cb.select() if mails['remember'] == '1' else cb.deselect()
        self.rem = rem

    def submit(self):
        if self.pwd.get() == rpwd():
            return self._save()
        vpwd = tk.StringVar()
        top = tk.Toplevel()
        top.title('Verify')
        mh, mw = top.maxsize()
        top.geometry(f'+{round(mh//3)}+{round(mw//3)}')
        def ver():
            if vpwd.get() == self.pwd.get():
                self._save()
                top.destroy()
            else:
                tk.showwarning('Password must be matched')
        tk.Entry(top, cnf={'textvariable':vpwd}, show='*').grid(row=0)
        tk.Button(top, text='Submit', command = ver).grid(row=1)
        top.mainloop()
        self.master.destroy()

    def _save(self):
        mails['email'] = self.email.get()
        mails['remember'] = str(self.rem.get())
        config.pwd(self.pwd.get())
        self.master.destroy()
        config.update()
        return 0
