import math
from time import strftime
from dateutil.parser import parse
from threading import Thread
from collections import deque

from srml import Parse

from . import tk


__all__ = ('SelectFrame',)
class Page(object):
    def __init__(self, content, pagen = 10):
        self.ctt = content
        self.n = pagen
        self.inited = False
        thr = Thread(target = self.init)
        thr.setDaemon(True)
        thr.start()

    def init(self):
        de = self.de = deque()
        ap = de.append
        for i in self.ctt:
            ap(i)
        self.inited = True

    @property
    def length(self):
        return len(self.de)

    @property
    def pages(self):
        return math.ceil(self.length // self.n)

    def page(self, page):
        n = self.n
        page += 1
        for a in range(page * n, page * n + n):
            try:
                yield self[a]
            except IndexError:
                break

    def __getitem__(self, index):
        if not index < self.length:
            if self.inited:
                raise IndexError('No so much items')
            else:
                while True:
                    try:
                        return self.de[index]
                    except:
                        if self.inited:
                            raise IndexError('No so much items')
                        else:
                            pass
        else:
            return self.de[index]

class SelectFrame(tk.Frame):
    def __init__(self, gls, master, box):
        super().__init__(master)
        self.gls = gls
        self.imap = box.imap
        self.items = []
        self.pack()

        self.crt_items()

    def crt_items(self):
        self.delits()
        folders = self.imap.list_folders()
        def binder(fold):
            return lambda e: self.select(fold)
        its = self.items = []
        for i, f in enumerate(folders):
            fold = f[-1]
            l = tk.Label(self, text = fold, font=('', 15, ''))
            l.grid(row = i, sticky = tk.W)
            its.append(l)
            l.bind("<Button>", binder(fold))

    def delits(self):
        its = self.items
        while its:
            its.pop().destroy()

    def inbox(self):
        fs = self.imap.list_folders()
        self.select(fs[0][-1])

    def select(self, fold):
        self.delits()
        self.imap.select_folder(fold)
        f = Folder(self)
        f.grid()
        self.items = [f]
        self.update()

class Folder(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.imap = master.imap
        msgs = self.list_folder()
        self.page = Page(msgs)
        self.items = []
        self.pagec()
        self.crt_items()

    def read(self, par):
        self.master.gls['Reader'](self.master.gls, par)

    def back(self):
        self.master.crt_items()

    def delits(self):
        its = self.items
        while its:
            its.pop().destroy()
        self.update()

    def crt_items(self, page = 0):
        self.delits()
        back = tk.Label(self, text = '<- Back', cursor = 'sb_left_arrow')
        back.grid(row = 0, sticky = tk.W)
        back.bind('<Button>', lambda e: self.back())
        self.update()
        self.updatepage()
        self.master.update()

        a = 1
        page = self.page.page(page)

        def binder(p):
            return lambda e: self.read(p)

        i = 0
        for p in page:
            di = p.dict()
            stri = self.stri

            ti = stri(di['Subject']) + ' from ' + stri(di['From'])
            l1 = tk.Label(self, text = ti, cursor = 'hand1', bg='white')
            l2 = tk.Label(self, text = self.pt(di['Date']), fg='gray')

            l1.grid(row = i + a, column = 0, pady = 5)
            l2.grid(row = i + a, column = 1, sticky = tk.W, pady = 5)

            l1.bind("<Button>", binder(p))

            self.items.extend((l1, l2))
            self.update()
            self.master.update()
            i += 1
        else:
            self.update()
            self.updatepage()
        if i == 0:
            tk.Label(self, text="There's nothing here...", font=('', 15 , '')).grid(row = 1)

    def pagec(self):
        F = self.F = tk.Frame(self)
        F.grid(row = self.page.n + 2)
        
        tk.Label(F, text='pages:').grid(row = 0, column = 0)
        items = F.its = []

    def delfits(self):
        its = self.F.its
        while its:
            its.pop().destroy()

    def updatepage(self):
        try:
            F = self.F
        except AttributeError:
            self.pagec()
            F = self.F
        self.delfits()
        def gb(page):
            return lambda : self.crt_items(page)
        items = F.its
        for a in range(self.page.pages):
            btn = tk.Button(F, text = str(a + 1), command = gb(a))
            btn.grid(row = 0, column = a + 1)
            items.append(btn)
        F.update()
        self.update()

    @staticmethod
    def pt(time):
        t = parse(time)
        ft = '%Y/%m/%d %A, %H:%M'
        return t.strftime(ft)

    def list_folder(self):
        imap = self.imap
        try:
            for uid in imap.search('ALL')[::-1]:
                bmsg = imap.fetch(uid)[b'BODY[]']
                yield Parse(bmsg)
        except:
            imap.update()
            yield from self.list_folder()

    @staticmethod
    def stri(b):
        if isinstance(b, str):
            return b
        elif isinstance(b, (bytes, bytearray)):
            return b.decode()
        else:
            return str(b)
