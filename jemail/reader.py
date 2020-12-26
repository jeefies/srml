from . import tk

__all__ = ('Reader',)

def Reader(gls, par):
    top = tk.Toplevel(tk.root)
    top.geometry('+100+100')
    rf = ReaderFrame(gls, top, par)
    rf.pack()
    top.resizable(0,0)
    top.mainloop()

class ReaderFrame(tk.Frame):
    def __init__(self, gls, master, par):
        super().__init__(master)
        self.gls = gls
        self.par = par

        self.crt_items()

    def crt_items(self):
        msg = self.par
        di = msg.dict()
        tk.Font(self, name = 'sub', size = 12, weight = tk.ttf.BOLD)

        # Subject
        tk.Label(self, text = di['Subject'], font='sub').grid(row = 0, column = 0, columnspan = 2)
        
        # From
        tk.Label(self, text = 'From:').grid(row = 1, column = 0)
        tk.Label(self, text = di['From']).grid(row = 1, column =  1)
        
        # To
        tk.Label(self, text = "To:").grid(row = 2, column = 0)
        tk.Label(self, text = di['To']).grid(row = 2, column = 1)
        
        # Date
        tk.Label(self, text = 'Date:').grid(row = 3, column = 0)
        tk.Label(self, text = di['Date']).grid(row = 3, column = 1)
        
        # Text
        text = tk.Text(self, width = 50)
        text.insert('0.0', msg.body)
        text.grid(row = 4, column = 0, columnspan = 2, padx = 10, pady = 5)
        text['state'] = 'disable'
        text.update()

        self.update()
