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
    
def ConcatConfig(gls):
    top = tk.Toplevel()
    h, w = top.maxsize()
    top.title('Concats config')
    top.geometry(f'{h // 2}x{w // 2}+{h // 4}+{h // 4}')
    _ConcatConfig(top, gls).pack()
    top.mainloop()
    
class _ConcatConfig(tk.Frame):
    def __init__(self, master, gls):
        super().__init__(master)
        self.gls = gls
        self.crt_item()
    
    def crt_item(self):
        tk.Button(self, text = 'Add', command = self.new).grid(row = 0)
        ccs = config.concats
        ad = 1
        for i, c in enumerate(ccs):
            info = c + ' : ' + css[c]
            tk.Label(self, text = info).grid(row = i + ad, column=0)
            tk.Button(self, text = 'modify', command = lambda : self.modify(c))\
                .grid(row = i + ad, column = 1)
            
    def modify(self, c):
        ccs = config.concats
        def mod(name, email, top):
            n, e = name.get(), email.get()
            if not (n and e):
                tk.showwarning('None content', \
                              "Please don not enter nothing")
                return 1
            if n in ccs:
                ccs[n] = e
            else:
                del ccs[c]
                ccs[n] = e
            config.update()
            top.destroy()
            tk.showinfo('Concat', 'Modify Success')
        self._g(mod, c, css[c])
    
    def add(self):
        ccs = config.concats
        def add(name, email, top):
            n, e = name.get(), email.get()
            if n and e:
                if e in ccs:
                    tk.showwarning('Unique Name',\
                                   'Concat name can not be the same, or use modify for it')
                    return 1
                ccs[n] = e
            else:
                tk.showwarning('NULL Content', 'Name and Email must not be nothing')
                return 1
            config.update()
            top.destroy()
            tk.showinfo('Concat', 'Add success')
        self._g(add)
            
    def _g(self, cmd, valn = '', vale = ''):
        top = tk.Toplevel()
        name, email = tk.StringVar(), tk.StringVar()
        name.set(valn)
        email.set(vale)
        tk.Label(top, text="Name").grid(row = 0)
        tk.Entry(top, cnf={'textvariable': name}).grid(row = 1)
        tk.Label(top, text = 'Email Address').grid(row = 2)
        tk.Entry(top, cnf={'textvariable': email}).grid(row = 3)
        tk.Button(top, text = 'ADD', command = lambda : cmd(name, email, top))\
            .grid(row = 4)
        top.mainloop()
       
