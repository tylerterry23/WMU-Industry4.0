from tkinter import *

class LoginWindow:
    def __init__(self):
        # This could be done better
        # Naive way of determining how the program should handle the login:
        # 0: Guest User (Student View)
        # 1: Admin
        # 2: Closed Window
        self.output = None 

        # Creates the login window
        self.win=Tk()
        self.win.geometry('450x150')
        self.win.maxsize(450,150)
        self.win.title("Industry 4.0 Lab Login")
        
        # Creates the widgets for the window
        self.PlaceWidgets()
       
        # Create Closing Protocol
        self.win.protocol("WM_DELETE_WINDOW", self.Close)
        
        # Bind enter Key
        self.win.bind('<Return>', lambda event: self.Check_Pass())

        # Main loop for the window
        self.win.mainloop()


    def PlaceWidgets(self):
        
        # The Title label
        self.titlelab = Label(self.win, text="Industry 4.0 Lab Login", pady=10)
        self.titlelab.configure(font=("Times", 20, "bold")) 
        self.titlelab.grid(row=0,column=0, columnspan=3)
        
        # Placing the password label and entry window
        self.passwordlab = Label(self.win, text='Admin Password', padx=20).grid(row=1, column=0)
        self.password = StringVar()
        self.passentry = Entry(self.win, textvariable=self.password, show='*', width=10)
        self.passentry.grid(row=1, column=2, padx=100)
        
        # Empty label to be updated after validating login
        self.loginlabel = Label(self.win, text='', pady=10)
        self.loginlabel.grid(row=3,column=2)
        
        # Button for loging in as admin
        self.button1 = Button(self.win, text='Login', command=self.Check_Pass).grid(row=4, column=0)
    
        # Label for deco
        self.label1 = Label(self.win, text='or').grid(row=4, column=1, padx=10)

        # Places the buttons for entering as a student
        self.button2 = Button(self.win, text='Enter as a student', command=self.GuestLogin).grid(row=4, column=2)
  

    def Check_Pass(self):

        if self.passentry.get() == '9697':
            self.output = 1
            self.win.destroy()
        else:
            self.loginlabel.configure(text='Unsuccessful Login')

    def GuestLogin(self):
        self.output = 0
        self.win.destroy()

    def Close(self):
        self.output = 2
        self.win.destroy()


