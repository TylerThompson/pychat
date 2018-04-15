import tkinter as tk
import tkinter.scrolledtext as tkst

class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

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
        #
        method_to_call = getattr(self.frames[page_name], 'build')
        method_to_call()



class ForgotPassPage(tk.Frame):
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        tk.Frame.__init__(self, self.parent)

    def build(self):
        # Destroy previous versions of forgot password
        for widget in self.winfo_children():
            widget.destroy()

        self.parent.grid(row=0, column=0)
        label = tk.Label(self, text="This is the forgot password page")
        label.pack(side="top", fill="x", pady=10)
        register = tk.Button(self, text="Register", command=lambda: self.controller.show_frame("RegisterPage"))
        login = tk.Button(self, text="Login", command=lambda: self.controller.show_frame("LoginPage"))
        register.pack()
        login.pack()

class ChatPage(tk.Frame):
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

        # Button for exiting
        self.exit_button = tk.Button(frame03, text='Exit')
        #self.exit_button.bind('<Button-1>', self.exit_event)

        # Positioning widgets in frame
        self.messages_list.pack(fill=tk.BOTH, expand=tk.YES)
        self.logins_list.pack(fill=tk.BOTH, expand=tk.YES)
        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
        self.send_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
        self.exit_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

        #label = tk.Label(self, text="This is the chat page")
        #label.pack(side="top", fill="x", pady=10)
        #button = tk.Button(self, text="Logout", command=lambda: controller.show_frame("LoginPage"))
        #button.pack()

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        tk.Frame.__init__(self, self.parent)

    def build(self):
        # Destroy previous versions of page
        for widget in self.winfo_children():
            widget.destroy()

        self.parent.grid(row=0, column=0)
        label = tk.Label(self, text="This is the login page")
        label.pack(side="top", fill="x", pady=10)
        register = tk.Button(self, text="Register", command=lambda: self.controller.show_frame("RegisterPage"))
        login = tk.Button(self, text="Login", command=lambda: self.controller.show_frame("ChatPage"))
        forgot = tk.Button(self, text="Forgot Password", command=lambda: self.controller.show_frame("ForgotPassPage"))
        register.pack()
        login.pack()
        forgot.pack()


class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        tk.Frame.__init__(self, self.parent)

    def build(self):
        # Destroy previous versions of register page
        for widget in self.winfo_children():
            widget.destroy()

        self.parent.grid(row=0, column=0)
        label = tk.Label(self, text="This is the register page")
        label.pack(side="top", fill="x", pady=10)
        login = tk.Button(self, text="Login", command=lambda: self.controller.show_frame("LoginPage"))
        forgot = tk.Button(self, text="Forgot Password", command=lambda: self.controller.show_frame("ForgotPassPage"))
        login.pack()
        forgot.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
