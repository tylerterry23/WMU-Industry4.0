from tkinter import *
from tkinter import ttk

class HelpWindow:
    def __init__(self, page):
        self.page = page

        # Used to force the window above all other windows.
        self.win = Toplevel()
        self.win.title('Help')
        self.win.geometry('600x400')
        self.win.resizable(False, False)


        if page == 'home':
            with open('main_app\GUI\\backend\HomeHelp.txt', 'r') as f:
                self.text_input = f.read()
            self.home()

        
    def home(self):
        self.frame = Frame(self.win)
        self.frame.pack()

        self.text = Text(self.frame, width=600, height=400, wrap=WORD)
        self.text.pack()
        self.text.insert(END, self.text_input)




