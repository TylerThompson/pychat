import tkinter as tk
import tkinter.scrolledtext as tkst
from PIL import Image, ImageTk
import os

class PyChatApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Set the title of the app
        self.title = "PyChat"
        self.wm_title("PyChat")
        # Change the icon
        imageIcon = '@pychat_2d5_icon.xbm'
        if os.name == 'nt':
            imageIcon = 'pychat_2d5_icon.ico'
        self.iconbitmap(imageIcon)
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        # Set all frames
        self.frames = {}
        for F in (LoginPage, RegisterPage, ChatPage, ForgotPassPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            # Stack the frames on top of each other
            frame.grid(row=0, column=0, sticky="nsew")
        # Show login first
        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        for frame in self.frames.values():
            frame.grid_remove()
        frame = self.frames[page_name]
        frame.grid()
        # Call build
        method_to_call = getattr(self.frames[page_name], 'build')
        method_to_call()

class ForgotPassPage(tk.Frame):
    ''' Forgot password page'''
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        tk.Frame.__init__(self, self.parent)

    def build(self):
        # Destroy previous versions of forgot password
        for widget in self.winfo_children():
            widget.destroy()

        self.parent.grid(row=0, column=0)
        # Set label of page
        forgotPassLabel = tk.Label(self, text='Forgot Password')
        forgotPassLabel.pack(side="top", fill="x", pady=(30, 10))
        # Set email
        email = tk.Entry(self, width=20)
        email.insert(0, 'Email')
        email.focus_set()
        email.pack(side="top", fill="x", pady=(30, 10))
        # Change Password
        password = tk.Entry(self, width=20, text='Password', show='*')
        password.insert(0, 'Password')
        password.pack(side="top", fill="x", pady=5)
        # Confirm password
        password2 = tk.Entry(self, width=20, text='Password', show='*')
        password2.insert(0, 'Password')
        password2.pack(side="top", fill="x", pady=5)
        # Change password button
        forgotPassBtn = tk.Button(self, text='Forgot Password', bg='#0084ff', activebackground='#0084ff', activeforeground='white', foreground='white')
        forgotPassBtn.pack(side="top", fill="x", pady=(40, 10))
        # button.bind('<Return>', self.get_login_event)
        loginBtn = tk.Button(self, text='Login', command=lambda: self.controller.show_frame("LoginPage"))
        loginBtn.pack(side="top", fill="x", pady=(5, 5))
        # button.bind('<Button-1>', self.get_register_event)
        registerBtn = tk.Button(self, text='Register', borderwidth=0, command=lambda: self.controller.show_frame("RegisterPage"))
        registerBtn.pack(side="top", fill="x", pady=(5, 10))

class ChatPage(tk.Frame):
    ''' Chat Page'''
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        tk.Frame.__init__(self, self.parent)

    def build(self):
        # Destroy previous versions of chat, or login
        for widget in self.winfo_children():
            widget.destroy()

        self.parent.grid(row=0, column=0)
        self.parent.rowconfigure(0, weight=1)
        self.parent.columnconfigure(0, weight=1)
        # List of messages
        frame00 = tk.Frame(self.controller)
        frame00.grid(column=0, row=0, rowspan=2, sticky="nsew")
        # List of Active users
        frame01 = tk.Frame(self.controller)
        frame01.grid(column=1, row=0, rowspan=3, sticky="nsew")
        # Message entry
        frame02 = tk.Frame(self.controller)
        frame02.grid(column=0, row=2, columnspan=1, sticky="nsew")
        # Buttons
        frame03 = tk.Frame(self.controller)
        frame03.grid(column=0, row=3, columnspan=2, sticky="nsew")
        # Set the position of the windows
        self.controller.rowconfigure(0, weight=1)
        self.controller.rowconfigure(1, weight=1)
        self.controller.rowconfigure(2, weight=8)
        self.controller.columnconfigure(0, weight=1)
        self.controller.columnconfigure(1, weight=1)

        # ScrolledText widget for displaying messages
        self.messages_list = tkst.ScrolledText(frame00, wrap=tk.WORD, height=20)
        self.messages_list.insert(tk.END, 'Welcome to Python Chat\n')
        self.messages_list.configure(state='disabled')

        # Listbox widget for displaying active users and selecting them
        self.logins_list = tk.Listbox(frame01, selectmode=tk.SINGLE, exportselection=False)
        #self.logins_list.bind('<<ListboxSelect>>', self.selected_login_event)

        # Entry widget for typing messages in
        self.entry = tk.Text(frame02)
        self.entry.focus_set()
        #self.entry.bind('<Return>', self.send_entry_event)

        # Button widget for sending messages
        self.send_button = tk.Button(frame03, text='Send')
        #self.send_button.bind('<Button-1>', self.send_entry_event)

        # Positioning widgets in frame
        self.messages_list.pack(fill=tk.BOTH, expand=tk.YES)
        self.logins_list.pack(fill=tk.BOTH, expand=tk.YES)
        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
        self.send_button.pack(side=tk.RIGHT, fill=tk.BOTH, expand=tk.YES)

class LoginPage(tk.Frame):
    ''' Login Page '''
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        tk.Frame.__init__(self, self.parent)

    def build(self):
        # Destroy previous versions of page
        for widget in self.winfo_children():
            widget.destroy()

        self.parent.grid(row=0, column=0)
        load = Image.open('PyChat.png')
        render = ImageTk.PhotoImage(load)
        logo = tk.Label(self, image=render)
        logo.image = render
        logo.pack(side="top", fill="x", pady=20)

        email = tk.Entry(self, width=20)
        email.insert(0, 'Email')
        email.focus_set()
        email.pack(side="top", fill="x")

        password = tk.Entry(self, width=20, text='Password', show='*')
        password.insert(0, 'Password')
        password.pack(side="top", fill="x", pady=5)

        loginBtn = tk.Button(self, text='Login', bg='#0084ff', activebackground='#0084ff', activeforeground='white', foreground='white', command=lambda: self.controller.show_frame("ChatPage"))
        loginBtn.pack(side="top", fill="x")
        #button.bind('<Return>', self.get_login_event)

        registerBtn = tk.Button(self, text='Register', command=lambda: self.controller.show_frame("RegisterPage"))
        registerBtn.pack(side="top", fill="x")
        #button.bind('<Button-1>', self.get_register_event)

        forgotBtn = tk.Button(self, text='Forgot Password', borderwidth=0, command=lambda: self.controller.show_frame("ForgotPassPage"))
        forgotBtn.pack(side="top", fill="x")

        copy = tk.Label(self, text='PyChat © 2018', width=20)
        copy.pack(side="top", fill="x", pady=(100, 10))

class RegisterPage(tk.Frame):
    ''' Registration Page'''
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        tk.Frame.__init__(self, self.parent)

    def build(self):
        # Destroy previous versions of register page
        for widget in self.winfo_children():
            widget.destroy()

        self.parent.grid(row=0, column=0)

        load = Image.open('PyChat.png')
        render = ImageTk.PhotoImage(load)
        logo = tk.Label(self, image=render)
        logo.image = render
        logo.pack(side="top", fill="x", pady=20)

        name = tk.Entry(self, width=20)
        name.insert(0, 'Full name')
        name.focus_set()
        name.pack(side="top", fill="x", pady=5)

        username = tk.Entry(self, width=20)
        username.insert(0, 'Username')
        username.focus_set()
        username.pack(side="top", fill="x", pady=5)

        email = tk.Entry(self, width=20)
        email.insert(0, 'Email')
        email.focus_set()
        email.pack(side="top", fill="x", pady=5)

        password = tk.Entry(self, width=20, text='Password', show='*')
        password.insert(0, 'Password')
        password.pack(side="top", fill="x", pady=5)

        registerBtn = tk.Button(self, text='Register', bg='#0084ff', activebackground='#0084ff', activeforeground='white', foreground='white')
        registerBtn.pack(side="top", fill="x")

        loginBtn = tk.Button(self, text='Login', command=lambda: self.controller.show_frame("LoginPage"))
        loginBtn.pack(side="top", fill="x")

        forgotBtn = tk.Button(self, text='Forgot Password', borderwidth=0, command=lambda: self.controller.show_frame("ForgotPassPage"))
        forgotBtn.pack(side="top", fill="x", pady=10)

        copy = tk.Label(self, text='PyChat © 2018', width=20)
        copy.pack(side="top", fill="x", pady=(90, 10))



if __name__ == "__main__":
    app = PyChatApp()
    app.mainloop()
