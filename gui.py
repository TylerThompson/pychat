from tkinter import *
import threading
from tkinter import scrolledtext
from tkinter import messagebox
from PIL import Image, ImageTk
import os

ENCODING = 'utf-8'

class GUI(threading.Thread):
    def __init__(self, client):
        super().__init__(daemon=False, target=self.run)
        self.font = ('Helvetica', 13)
        self.client = client
        self.login_window = None
        self.main_window = None
        self.frames = {}
        self.runLogin = False
        self.keepTrying = True

    def run(self):
        # Build the frame set for changing windows
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        # Ready all possible pages to be displayed
        for F in (LoginPage, RegisterPage, ChatPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
        # Put pages in same location
        frame.grid(row=0, column=0, sticky="nsew")

        while self.keepTrying:
            if self.runLogin:
                self.show_frame("LoginPage")
                #self.login_window = LoginWindow(self, self.font)
            else:
                self.show_frame("RegisterPage")
                #self.login_window = RegisterWindow(self, self.font)

        self.show_frame("ChatPage")
        #self.main_window = ChatWindow(self, self.font)
        self.notify_server(self.login_window.login, 'login')
        #self.main_window.run()

    def show_frame(self, page_name):
        ''' Show a frame for the given page'''
        frame = self.frames[page_name]
        frame.tkraise()

    @staticmethod
    def display_alert(message):
        """Display alert box"""
        messagebox.showinfo('Error', message)

    def update_login_list(self, active_users):
        """Update login list in main window with list of users"""
        self.main_window.update_login_list(active_users)

    def display_message(self, message):
        """Display message in ChatWindow"""
        self.main_window.display_message(message)

    def send_message(self, message):
        """Enqueue message in client's queue"""
        self.client.queue.put(message)

    def set_target(self, target):
        """Set target for messages"""
        self.client.target = target

    def notify_server(self, message, action):
        """Notify server after action was performed"""
        data = action + ";" + message
        data = data.encode(ENCODING)
        self.client.notify_server(data, action)

    def login(self, login):
        self.client.notify_server(login, 'login')

    def logout(self, logout):
        self.client.notify_server(logout, 'logout')

class Window(object):
    def __init__(self, title, font):
        self.root = Tk()
        if os.name == 'nt':
            self.root.iconbitmap('pychat_2d5_icon.ico')
        else:
            self.root.iconbitmap('@pychat_2d5_icon.xbm')
        self.title = title
        self.root.title(title)
        self.font = font

class RegisterWindow(Window):
    def __init__(self, gui, font):
        super().__init__("PyChat Login", font)
        self.gui = gui
        self.label = None
        self.entry = None
        self.button = None
        self.login = None
        self.img = None

        self.build_window()
        self.run()

    def build_window(self):
        """Build login window, , set widgets positioning and event bindings"""
        self.root.geometry('200x400')
        self.root.minsize(200, 400)
        self.root.maxsize(200, 400)
        # Set the image

        self.input_size = 19

        load = Image.open('PyChat.png')
        render = ImageTk.PhotoImage(load)
        self.label = Label(self.root, image=render)
        self.label.image = render
        self.label.place(x=40, y=10)

        # Full Name
        self.entry = Entry(self.root, width=self.input_size, font=self.font)
        self.entry.insert(0, 'Full Name')
        self.entry.focus_set()
        self.entry.place(x=1, y=150)

        # Email
        self.entry = Entry(self.root, width=self.input_size, font=self.font)
        self.entry.insert(0, 'Email')
        self.entry.place(x=1, y=180)

        # Username
        self.entry = Entry(self.root, width=self.input_size, font=self.font)
        self.entry.insert(0, 'Username (a-z0-9)')
        self.entry.place(x=1, y=210)

        # Password
        self.entry = Entry(self.root, width=self.input_size, font=self.font, text='Password', show='*')
        self.entry.insert(0, 'Password')
        self.entry.place(x=1, y=240)

        self.button = Button(self.root, text='Register', font=self.font)
        self.button.place(x=105, y=300)
        self.button.bind('<Button-1>', self.send_register_event)

        self.button = Button(self.root, text='Login', font=self.font)
        self.button.place(x=1, y=300)
        self.button.bind('<Button-2>', self.get_login_event)

        self.label = Label(self.root, text='PyChat © 2018', width=20, font=self.font)
        self.label.place(x=0, y=380)

    def run(self):
        """Handle login window actions"""
        self.root.mainloop()
        self.root.destroy()

    def get_login_event(self):
        print("you clicked login on register window")

    def send_register_event(self):
        '''something todo'''


class LoginWindow(Window):
    def __init__(self, gui, font):
        super().__init__("PyChat Login", font)
        self.gui = gui
        self.label = None
        self.entry = None
        self.button = None
        self.login = None
        self.img = None

        self.build_window()
        self.run()

    def build_window(self):
        """Build login window, , set widgets positioning and event bindings"""
        self.root.geometry('200x400')
        self.root.minsize(200, 400)
        self.root.maxsize(200, 400)

        load = Image.open('PyChat.png')
        render = ImageTk.PhotoImage(load)
        self.label = Label(self.root, image=render)
        self.label.image = render
        self.label.place(x=40, y=10)

        self.entry = Entry(self.root, width=20, font=self.font)
        self.entry.insert(0, 'Email')
        self.entry.focus_set()
        self.entry.place(x=0, y=155)

        self.entry = Entry(self.root, width=20, font=self.font, text='Password', show='*')
        self.entry.insert(0, 'Password')
        self.entry.place(x=0, y=185)

        self.button = Button(self.root, text='Login', font=self.font)
        self.button.place(x=125, y=220)
        self.button.bind('<Return>', self.get_login_event)

        self.button = Button(self.root, text='Register', font=self.font)
        self.button.place(x=0, y=220)
        self.button.bind('<Button-1>', self.get_register_event)

        self.label = Label(self.root, text='PyChat © 2018', width=20, font=self.font)
        self.label.place(x=0, y=380)

    def run(self):
        """Handle login window actions"""
        self.root.mainloop()
        self.root.destroy()

    def get_login_event(self, event):
        """Get login from login box and close login window"""
        self.login = self.entry.get()
        self.root.quit()

    def get_register_event(self, event):
        ''' Get register to display'''
        #self.login_window = None
        #self.root.mainloop()

        self.login_window = RegisterWindow(self, self.font)
        #self.root.quit()


class ChatWindow(Window):
    def __init__(self, gui, font):
        super().__init__("Python Chat", font)
        self.gui = gui
        self.messages_list = None
        self.logins_list = None
        self.entry = None
        self.send_button = None
        self.exit_button = None
        self.lock = threading.RLock()
        self.target = ''
        self.login = self.gui.login_window.login

        self.build_window()

    def build_window(self):
        """Build chat window, set widgets positioning and event bindings"""
        # Size config
        self.root.geometry('750x500')
        self.root.minsize(600, 400)

        # Frames config
        main_frame = Frame(self.root)
        main_frame.grid(row=0, column=0, sticky=N + S + W + E)

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # List of messages
        frame00 = Frame(main_frame)
        frame00.grid(column=0, row=0, rowspan=2, sticky=N + S + W + E)

        # List of logins
        frame01 = Frame(main_frame)
        frame01.grid(column=1, row=0, rowspan=3, sticky=N + S + W + E)

        # Message entry
        frame02 = Frame(main_frame)
        frame02.grid(column=0, row=2, columnspan=1, sticky=N + S + W + E)

        # Buttons
        frame03 = Frame(main_frame)
        frame03.grid(column=0, row=3, columnspan=2, sticky=N + S + W + E)

        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=8)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # ScrolledText widget for displaying messages
        self.messages_list = scrolledtext.ScrolledText(frame00, wrap='word', font=self.font)
        self.messages_list.insert(END, 'Welcome to Python Chat\n')
        self.messages_list.configure(state='disabled')

        # Listbox widget for displaying active users and selecting them
        self.logins_list = Listbox(frame01, selectmode=SINGLE, font=self.font,
                                      exportselection=False)
        self.logins_list.bind('<<ListboxSelect>>', self.selected_login_event)

        # Entry widget for typing messages in
        self.entry = Text(frame02, font=self.font)
        self.entry.focus_set()
        self.entry.bind('<Return>', self.send_entry_event)

        # Button widget for sending messages
        self.send_button = Button(frame03, text='Send', font=self.font)
        self.send_button.bind('<Button-1>', self.send_entry_event)

        # Button for exiting
        self.exit_button = Button(frame03, text='Exit', font=self.font)
        self.exit_button.bind('<Button-1>', self.exit_event)

        # Positioning widgets in frame
        self.messages_list.pack(fill=BOTH, expand=YES)
        self.logins_list.pack(fill=BOTH, expand=YES)
        self.entry.pack(side=LEFT, fill=BOTH, expand=YES)
        self.send_button.pack(side=LEFT, fill=BOTH, expand=YES)
        self.exit_button.pack(side=LEFT, fill=BOTH, expand=YES)

        # Protocol for closing window using 'x' button
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing_event)

    def run(self):
        """Handle chat window actions"""
        self.root.mainloop()
        self.root.destroy()

    def selected_login_event(self, event):
        """Set as target currently selected login on login list"""
        target = self.logins_list.get(self.logins_list.curselection())
        self.target = target
        self.gui.set_target(target)

    def send_entry_event(self, event):
        """Send message from entry field to target"""
        text = self.entry.get(1.0, END)
        if text != '\n':
            message = 'msg;' + self.login + ';' + self.target + ';' + text[:-1]
            print(message)
            self.gui.send_message(message.encode(ENCODING))
            self.entry.mark_set(INSERT, 1.0)
            self.entry.delete(1.0, END)
            self.entry.focus_set()
        else:
            messagebox.showinfo('Warning', 'You must enter non-empty message')

        with self.lock:
            self.messages_list.configure(state='normal')
            if text != '\n':
                self.messages_list.insert(END, text)
            self.messages_list.configure(state='disabled')
            self.messages_list.see(END)
        return 'break'

    def exit_event(self, event):
        """Send logout message and quit app when "Exit" pressed"""
        self.gui.notify_server(self.login, 'logout')
        self.root.quit()

    def on_closing_event(self):
        """Exit window when 'x' button is pressed"""
        self.exit_event(None)

    def display_message(self, message):
        """Display message in ScrolledText widget"""
        with self.lock:
            self.messages_list.configure(state='normal')
            self.messages_list.insert(END, message)
            self.messages_list.configure(state='disabled')
            self.messages_list.see(END)

    def update_login_list(self, active_users):
        """Update listbox with list of active users"""
        self.logins_list.delete(0, END)
        for user in active_users:
            self.logins_list.insert(END, user)
        self.logins_list.select_set(0)
        self.target = self.logins_list.get(self.logins_list.curselection())
