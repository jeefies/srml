import os

from . import tk

class Main(tk.Frame):
    def __init__(self, gls, box):
        super().__init__(tk.root)
        self.gls = gls
        self.box = box
        root = tk.root
        mw, mh = root.maxsize()
        root.geometry(f'{mw // 2}x{mh // 2}+{mw // 4}+{mh // 4}')

        self.create_menu()

        self.pack()
        
    def create_menu(self):
        mainmenu = tk.Menu(self)
        
        # menu file
        filemn = tk.Menu(mainmenu, tearoff=0)
        filemn.add_command(label = 'Open', command = self.askopen)
        filemn.add_command(label = 'Save', command = self.save)
        filemn.add_separator()
        filemn.add_command(label = 'Exit', command = self.exit)
        mainmenu.add_cascade(label = 'File', menu=filemn)
        
        # menu config
        configmn = tk.Menu(mainmenu, tearoff=0)
        configmn.add_command(label = 'User', command = self.modify)
        configmn.add_command(label = 'Concat', command = self.new)
        mainmenu.add_cascade(label = 'Config', menu=configmn)

        tk.root.config(menu = mainmenu)
        
    def new(self):
        pass
        
    def modify(self):
        self.gls['UserConfig'](self.gls)
        
    def askopen(self):
        fts = (('JE mail file', '.Jml'), ('TXT File', '.txt'), ('ALL File', '*'))
        file = tk.askopenfilename(parent=self, title='jemail', \
                initialdir=os.getcwd(), filetypes=fts)
        print(file)
        
    def exit(self):
        self.pack_forget()
        #self.master.desteroy()
        
    def save(self):
        pass
