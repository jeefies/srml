from . import tk, config

__all__ = ("Writer",)


def Writer(gls, box):
    root = tk.root
    top = tk.Toplevel(root)
    w, h = top.maxsize()
    top.geometry(f'700x500+{w // 6}+{h // 6}')
    top.resizable(0,0)
    wf = WriteFrame(gls, top, box)
    wf.pack()
    top.mainloop()

class WriteFrame(tk.Frame):
    def __init__(self, gls, master, box):
        super().__init__(master)
        self.mst = master
        self.box = box
        self.msg = box.createMessage()
        self.crt_items()

    def crt_items(self):
        # Concat show frame
        col = 4
        self.cc = cc = _Concats(self)
        cc.grid(column = col, rowspan = 3)

        # sender name entry
        tk.Label(self, text = "Send Name:").grid(row = 0, column = col - 3)
        tk.Label(self, text=self.msg.mail).grid(row = 0, column = col - 4)
        name = tk.StringVar()
        en = tk.Entry(self, width = 20)
        en['textvariable'] = name
        en.grid(row = 0, column = col - 2)
        self.ename = name

        # subject entry
        tk.Label(self, text = "Subject:").grid(row = 1, column = col - col)
        sub = tk.StringVar()
        en = tk.Entry(self, width = 50)
        sub.set('Subject')
        en['textvariable'] = sub
        en.grid(row = 1, column = col - 3, columnspan = 2)
        self.subject = sub

        # receiver entry
        tk.Label(self, text = "Receivers:").grid(row = 2, column = col - col)
        recv = _MailRecv(self, width = 50)
        recv.grid(row = 2, column = col - 3, columnspan = 2)
        self.erecv = recv

        # Content entry
        tk.Label(self, text = "Contents").grid(row = 3, column = col - col)
        ctx = tk.StringVar()
        text = tk.Text(self, width = 50)
        text.grid(row = 3, column = col - 3, columnspan = 2)
        self.ectx = text

    def add_cc(self, cc, v):
        if cc.val not in self.msg.recv:
            self.msg.recv.append(cc.val)
        else:
            self.msg.recv.remove(cc.val)
        self.erecv.iupdate()
        self.cc.iupdate()

    @property
    def ctx(self):
        return self.ectx.get('0.0', 'end')

    def prt(self, event = None):
        msg = self.msg
        sub = self.subject.get()
        ename = self.ename.get()
        msg.subject = sub
        msg.sendname(ename)
        msg.body = self.ctx

    def send(self):
        self.prt()
        try:
            self.box.send(self.msg)
        except:
            self.box.update()
            self.box.send(self.msg)
        self.clear()

    def clear(self):
        res = tk.askyesno('Sucess', 'Send Success!\nClear the Data?', parent = self.master)
        if res:
            self.subject.set('')
            self.ectx.delete('0.0', 'end')
            self.msg.recv = []
            self.erecv.iupdate()
            self.update()
        else:
            pass

class _MailRecv(tk.Entry):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        var = tk.StringVar()
        self['textvariable'] = var
        self.msg = master.msg
        self.var = var
        self.bind("<Key-Return>", self.info)

    def iupdate(self):
        var = self.var
        new = self.msg.recv
        now = set(new)
        var.set(' '.join(now))

    def info(self, event=None):
        var  = self.var
        msg = self.msg
        now = set(self.var.get().split())
        msg.recv = list(now)
        var.set(' '.join(now))

class _Concats(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.crt_items()

    def crt_items(self):
        tk.Label(self, text = "Concats:")
        ccs = config.Concats()
        self.btns = btns = []
        selected = self.master.msg.recv
        vars = [tk.IntVar() for _ in ccs]
        def add(i, v):
            oc = ccs.place(i)
            return lambda e: self.master.add_cc(oc, v)
        for i, var in enumerate(vars):
            oc = ccs.place(i)
            btn = tk.Checkbutton(self, variable = var, text = oc.key)
            if oc.val in selected:
                btn.select()
            btns.append(btn)
            btn.grid(row = i + 1)
            btn.bind("<Button>", add(i, var))
        btns.append(tk.Button(self, text = "Send", command = self.master.send))
        btns[-1].grid(row = len(btns))

    def iupdate(self):
        for btn in self.btns:
            btn.destroy()
        self.crt_items()
        self.update()
        self.master.update()

