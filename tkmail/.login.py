from . import tk

root = tk.root

class Login(tk.Frame):
    def __init__(self):
        super().__init__(root)
        self.pack()
        self.master.geometry('200x200+100+100')

        font = tk.Font(self, size=10, weight=tk.ttf.BOLD)

        tk.Label(self, text='Email', font=font).grid(row=0, column=0)

        email = tk.Entry(self, font=font)
        email.grid(row=1, column=0)
        self.email = tk.StringVar()
        email['textvariable'] = self.email

        tk.Label(self, text='Password', font=font).grid(row=2, column=0)
        
        pwd = tk.Entry(self, font=font, show='*')
        pwd.grid(row=3, column=0)
        self.pwd = tk.StringVar()
        pwd['textvariable'] = self.pwd

        tk.Label(self, text='Verify', font=font).grid(row=4, column=0)

        vpwd = tk.Entry(self, font=font, show='*')
        vpwd.grid(row=5, column=0)
        self.vpwd = tk.StringVar()
        vpwd['textvariable'] = self.vpwd

        btn = tk.Button(self, text = 'Submit', command=self.prt, font=font)
        btn.grid(row=6, column=0)


    def prt(self):
        #print(self.email.get())
        p = self.pwd.get()
        vp = self.vpwd.get()
        if not p == vp and p:
            tk.showerror('Password Error', "Two password must match")
        else:
            #print(p)
            self.pack_forget()
        self.pwd.set('')
        self.vpwd.set('')
