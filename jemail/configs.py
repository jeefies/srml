from . import tk
from .config import mails, rpwd
from . import config

__all__ = ('UserConfig', 'ConcatConfig')

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

        tk.Button(self, text="Logout", command = self.logout).grid(row=5)

        # submit
        btn = tk.Button(self, text = 'Submit', command=self.submit)
        btn.grid(row=6, column=0)

        # remember
        rem = tk.IntVar()
        cb = tk.Checkbutton(self, text='remember', variable=rem)
        cb.grid(row=6, column=1)
        nou = cb.select() if mails['remember'] == '1' else cb.deselect()
        self.rem = rem

    def logout(self):
        self.master.destroy()
        mails['remember'] = '0'
        config.update()
        self.gls['Login'](self.gls)

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
        btn = tk.Button(self, text = 'Add', command = self.new)
        btn.pack(side = 'top')
        self.ccf = _CCF(self)
        self.ccf.pack(side="bottom", fill="both")
            
    def modify(self, c):
        ccs = config.Concats()
        def mod(name, email, top):
            n, e = name.get(), email.get()
            if not (n and e):
                tk.showwarning('None content', \
                              "Please don not enter nothing",\
                              parent=self)
                return 1
            c1 = ccs[c]
            c1.key = n
            c1.val = e
            config.update()
            self.ccf.iupdate()
            top.destroy()
            tk.showinfo('Concat', 'Modify Success', parent = self)
        cc = ccs[c]
        self._g(mod, cc.key, cc.val, 'Modify')
    
    def new(self):
        ccs = config.Concats()
        def add(name, email, top):
            n, e = name.get(), email.get()
            if n and e:
                if e in ccs:
                    tk.showwarning('Unique Name',\
                                   'Concat name can not be the same, or use modify for it',\
                                   parent = self)
                    return 1
                ccs[n] = e
            else:
                tk.showwarning('NULL Content', 'Name and Email must not be nothing',\
                        parent = self)
                return 1
            config.update()
            top.destroy()
            tk.showinfo('Concat', 'Add success', parent = self)
            self.ccf.add()
        self._g(add)
            
    def _g(self, cmd, valn = '', vale = '', mod = "ADD"):
        top = tk.Toplevel(self.master)
        name, email = tk.StringVar(), tk.StringVar()
        name.set(valn)
        email.set(vale)
        tk.Label(top, text="Name").grid(row = 0)
        tk.Entry(top, cnf={'textvariable': name}).grid(row = 1)
        tk.Label(top, text = 'Email Address').grid(row = 2)
        tk.Entry(top, cnf={'textvariable': email}).grid(row = 3)
        tk.Button(top, text = mod, command = lambda : cmd(name, email, top))\
            .grid(row = 4)
        top.mainloop()
        self.iupdate()
       
    def iupdate(self):
        #try:
        #    self.ccf.init(self)
        #except:
        #    pass
        #self.ccf = _CCF(self)
        #self.ccf.pack(side="bottom", fill="both")
        'self.ccf.update()'

class _CCF(tk.Frame):
    def __init__(self, master):
        self.init(master)

    def init(self, master= None):
        super().__init__(master)
        ccs = config.Concats()
        def mod(i):
            oc = ccs.place(i)
            return lambda : master.modify(oc.key)
        def delete(i):
            oc = ccs.place(i)
            return lambda : self.delete(oc)
        for i, c in enumerate(ccs):
            tk.Label(self, textvariable = c.var).grid(row = i, column=0)
            tk.Button(self, text = 'modify', command = mod(i)).grid(row = i, column = 1)
            tk.Button(self, text = 'delete', command = delete(i)).grid(row = i, column = 2)
        self.i = i
        self.mst = master
        return self

    def delete(self, c):
        c.delete()
        config.update()
        self.iupdate()
        tk.showinfo('Delete', "Delete Success", parent = self.master.master)

    def iupdate(self):
        self.pack_forget()
        s = self.master
        s.ccf = _CCF(s)
        s.ccf.pack(fill='both', side='bottom')

    def add(self):
        self.iupdate()
