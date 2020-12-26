import io
import os
from threading import Thread

from . import tk, config

__all__ = ("Writer", 'WriteFrame', 'RWriter')


def Writer(gls, box):
    root = tk.root
    top = tk.Toplevel(root)
    w, h = top.maxsize()
    top.geometry(f'700x500+{w // 6}+{h // 6}')
    top.resizable(0,0)
    wf = WriteFrame(gls, top, box)
    wf.pack()
    top.mainloop()

def RWriter(gls, msg, box):
    root = tk.root
    top = tk.Toplevel(root)
    w, h = top.maxsize()
    top.geometry(f'700x500+{w // 6}+{h // 6}')
    top.resizable(0,0)
    wf = WriteFrame(gls, top, box, msg)
    wf.pack()
    wf.from_()
    top.mainloop()

class WriteFrame(tk.Frame):
    def __init__(self, gls, master, box, msg=None):
        super().__init__(master)
        self.gls = gls
        self.mst = master
        self.box = box
        self.msg = msg if msg else box.createMessage()
        self.crt_menu()
        self.crt_items()
        self.fts = (('JE mail file', '.Jml .Jmli .Jmln'.split()), ('TXT file', '.txt'),\
                ('All File', '*'))
        self.bind_all('<Control-o>', lambda e:self.open())

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

    def crt_menu(self):
        m = self.master
        mn = tk.Menu(m)

        # File tearoff
        fm = tk.Menu(mn, tearoff=0)
        ac = fm.add_command
        ac(label = 'Open', command = self.open)
        ac(label = 'Save', command = self.save)
        ac(label = 'New', command = self.new)
        fm.add_separator()
        ac(label = 'Exit', command = self.master.destroy)
        mn.add_cascade(label = "File", menu=fm)

        # Send command
        mn.add_command(label = 'Send', command = self.send)

        m.config(menu = mn)

    def add_cc(self, cc, v):
        if cc.val not in self.msg.recv:
            self.msg.recv.append(cc.val)
        else:
            self.msg.recv.remove(cc.val)
        self.erecv.iupdate()
        self.cc.iupdate()

    def open(self):
        name = tk.askopenfilename(parent = self, title='Open',\
                filetypes = self.fts, initialdir = os.getcwd())
        newmsg = self.msg.from_json(name)
        RWriter(self.gls, newmsg, self.box)

    def new(self):
        Writer(self.gls, self.box)

    def save(self):
        self.prt()
        f = io.StringIO()
        self.msg.to_json(fp = f)
        val = f.getvalue()
        name = tk.asksaveasfilename(parent = self, title='Save',\
                filetypes=self.fts, initialdir=os.getcwd())
        if not name:
            tk.showwarning("Save Error", "No file Select or Saved", parent = self)
            return
        with open(name, 'w') as f:
            f.write(val)

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

    def from_(self):
        msg = self.msg
        self.subject.set(msg.subject)
        self.ename.set(msg.sendname())
        self.ectx.insert('0.0', msg.body)
        self.erecv.iupdate()

    def send(self):
        self.prt()
        def _send():
            try:
                self.box.send(self.msg)
            except:
                self.box.update()
                self.box.send(self.msg)
            self.clear()
        thr = Thread(target=_send)
        thr.setDaemon(True)
        thr.start()

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

    def iupdate(self):
        for btn in self.btns:
            btn.destroy()
        self.crt_items()
        self.update()
        self.master.update()

