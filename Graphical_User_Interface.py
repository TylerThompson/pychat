import socket
import tkinter as tk
from tkinter import messagebox, Menu
import tkinter.scrolledtext as tkst
from PIL import Image, ImageTk
import threading
import select
import os


ENCODING = 'utf-8'
HOST = 'localhost'
PORT = 8080

class PyChatApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # Set the title of the app
        self.title = "PyChat"
        self.wm_title("PyChat")
        # Change the icon
        imageIcon = '@pychat_2d5_icon.xbm'
        if os.name == 'nt':
            imageIcon = 'pychat_2d5_icon.ico'
        self.iconbitmap(imageIcon)

        # Protocol for closing window using 'x' button
        self.protocol("WM_DELETE_WINDOW", self.on_closing_event)

        # Establish connection to server
        self.host = HOST
        self.port = PORT
        self.sock = None
        self.exit_event = False
        self.connected = self.connect_to_server()
        self.buffer_size = 1024
        self.username = None
        self.target = None
        self.messageBox = None
        self.loginList = None
        self.friendList = None
        self.lock = threading.RLock()


        # Check for client to exit
        if self.exit_event:
            exit()

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

    def setUsername(self, username):
        username = username.replace('\n', '')
        self.username = username

    def getUsername(self):
        return self.username

    def setTarget(self, target):
        target = target.replace('\n', '')
        self.target = target

    def getTarget(self):
        return self.target

    def setMessageBox(self, msgBox):
        self.messageBox = msgBox

    def getMessageBox(self):
        return self.messageBox

    def setLoginList(self, log):
        self.loginList = log

    def getLoginList(self):
        return self.loginList

    def setFriendList(self, log):
        self.friendList = log

    def getFiendList(self):
        return self.friendList

    def update_login_list(self, active_users):
        """Update listbox with list of active users"""
        login_list = self.getLoginList()
        login_list.delete(0, tk.END)
        for user in active_users:
            login_list.insert(tk.END, user)
        login_list.select_set(0)
        self.target = login_list.get(login_list.curselection())

    def update_friend_list(self, accepted_friends):
        """update friend list when friend is added or removed"""
        friend_list = self.getFiendList()
        for friends in accepted_friends:
            friend_list.insert(tk.END, friends)
        friend_list.select_set(0)
        self.target = friend_list.get(friend_list.curselection())


    def on_closing_event(self):
        print('closing event now')
        """ Let the server know that we are logging off"""
        try:
            message = "GUI|logout|" + self.username
            self.sock.send(message.encode(ENCODING))
            self.sock.close()
        except socket.error:
            print('there was an error sending logout')
        finally:
            exit()

    def set_target(self, target):
        """Set target for messages"""
        self.target = target

    def run(self):
        inputs = [self.sock]
        outputs = [self.sock]
        while inputs:
            try:
                read, write, exceptional = select.select(inputs, outputs, inputs)
            # if server unexpectedly quits, this will raise ValueError exception (file descriptor < 0)
            except ValueError:
                print('Server error')
                display_alert('Server error has occurred. Exit app')
                self.controller.sock.close()
                break

            if self.sock in read:
                with self.lock:
                    try:
                        data = self.sock.recv(self.buffer_size)
                    except socket.error:
                        print("Socket error")
                        display_alert('Socket error has occurred. Exit app')
                        self.sock.close()
                        break

                self.process_received_data(data)

            if self.sock in exceptional:
                print('Server error')
                display_alert('Server error has occurred. Exit app')
                self.sock.close()
                break

    def process_received_data(self, data):
        """Process received message from server"""
        print('got data from server: ' + str(data))
        data = data.decode(ENCODING)
        data = data.split('|', 4)

        method = data[1]

        # Process the method
        if method == 'msg':
            text = '<' + data[2] + '> ' + data[4]
            with self.lock:
                messagebox = self.getMessageBox()
                messagebox.configure(state='normal')
                messagebox.insert(tk.END, text)
                messagebox.configure(state='disabled')
                messagebox.see(tk.END)
        elif method == 'login_list':
            users = data[2]
            processed = users.split(';')
            self.update_login_list(processed)
        elif method == 'viewFriends':
            friends = data[2]
            processed = friends.split(';')
            self.update_friend_list(processed)

    def connect_to_server(self):
        """Connect to server via socket interface, return (is_connected)"""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((str(self.host), int(self.port)))
        except ConnectionRefusedError:
            display_alert("Server is inactive, unable to connect")
            self.exit_event = True
            return False
        return True

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        for frame in self.frames.values():
            frame.grid_remove()
        frame = self.frames[page_name]
        frame.grid()
        # Call build
        method_to_call = getattr(self.frames[page_name], 'build')
        method_to_call()


def display_alert(message):
    """Display alert box"""
    messagebox.showinfo('Warning', message)


class ForgotPassPage(tk.Frame):
    """ Forgot password page"""

    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        tk.Frame.__init__(self, self.parent)
        self.email = None
        self.password = None
        self.password2 = None

    def build(self):
        """ Build the forgot password page"""
        # Destroy previous versions of forgot password
        for widget in self.winfo_children():
            widget.destroy()

        self.parent.grid(row=0, column=0)
        # Set label of page
        forgotPassLabel = tk.Label(self, text='Forgot Password')
        forgotPassLabel.pack(side="top", fill="x", pady=(30, 10))
        # Set email
        self.email = tk.Entry(self, width=20)
        self.email.insert(0, 'Email')
        self.email.focus_set()
        self.email.pack(side="top", fill="x", pady=(30, 10))
        # Change Password
        self.password = tk.Entry(self, width=20, text='Password', show='*')
        self.password.insert(0, 'Password')
        self.password.pack(side="top", fill="x", pady=5)
        # Confirm password
        self.password2 = tk.Entry(self, width=20, text='Password', show='*')
        self.password2.insert(0, 'Password')
        self.password2.pack(side="top", fill="x", pady=5)
        # Change password button
        forgotPassBtn = tk.Button(self, text='Forgot Password', bg='#0084ff', activebackground='#0084ff', activeforeground='white', foreground='white', command=self.forgot)
        forgotPassBtn.pack(side="top", fill="x", pady=(40, 10))
        loginBtn = tk.Button(self, text='Login', command=lambda: self.controller.show_frame("LoginPage"))
        loginBtn.pack(side="top", fill="x", pady=(5, 5))
        # button.bind('<Button-1>', self.get_register_event)
        registerBtn = tk.Button(self, text='Register', borderwidth=0, command=lambda: self.controller.show_frame("RegisterPage"))
        registerBtn.pack(side="top", fill="x", pady=(5, 10))

    def forgot(self):
        """ Forgot password """
        email = self.email.get()
        password = self.password.get()
        password2 = self.password2.get()
        if password == password2:
            data = "GUI|forgot|" + email + "|" + password
            self.controller.sock.send(data.encode(ENCODING))
            data = self.controller.sock.recv(1024).decode(ENCODING)
            print('got data: ' + data)
            if "all" in data:
                display_alert("Password has been changed!")
            else:
                display_alert(str(data.split('|')[1]))
        else:
            display_alert("Passwords did not match!")


class ChatPage(tk.Frame):
    """ Chat Page"""
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.login = None
        self.entry = None
        self.messagebox = None
        self.target = None
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
        # list of Friends
        frame04 = tk.Frame(self.controller)
        frame04.grid(column=1, row=1, rowspan=2, sticky="nsew")
        # Message entry
        self.messagebox = tk.Frame(self.controller)
        self.messagebox.grid(column=0, row=2, columnspan=1, sticky="nsew")
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
        self.messages_list.insert(tk.END, 'Welcome to Python Chat, ' + self.controller.getUsername() + '\n')
        self.messages_list.configure(state='disabled')
        self.controller.setMessageBox(self.messages_list)

        # Listbox widget for displaying active users and selecting them
        self.logins_list = tk.Listbox(frame01, selectmode=tk.SINGLE, exportselection=False)
        self.logins_list.bind('<<ListboxSelect>>', self.selected_login_event)
        self.controller.setLoginList(self.logins_list)

        # Entry widget for typing messages in
        self.entry = tk.Text(self.messagebox, height=10)
        self.entry.focus_set()
        self.entry.bind('<Return>', self.send_entry_event)

        # Button widget for sending messages
        self.send_button = tk.Button(frame03, text='Send', bg='#0084ff', activebackground='#0084ff', activeforeground='white', foreground='white', command=lambda: self.send_entry_event)

        # Listbox widget for displaying friends and selecting them
        self.friends_list = tk.Listbox(frame04, selectmode=tk.SINGLE, exportselection=False)
        # self.friends_list.bind('<<ListboxSelect>>', self.option_menu_event)
        self.controller.setFriendList(self.friends_list)


        # Positioning widgets in frame
        self.messages_list.pack(fill=tk.BOTH, expand=tk.YES)
        self.logins_list.pack(fill=tk.BOTH, expand=tk.YES)
        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
        self.send_button.pack(side=tk.RIGHT, fill=tk.BOTH, expand=tk.YES)
        self.friends_list.pack(fill=tk.BOTH, expand=tk.YES)

        # Send request for current users
        self.controller.sock.send("update_login_list".encode(ENCODING))

        # Send request for current friends
        self.controller.sock.send("viewFriends".encode(ENCODING))

        # Run listeners for getting messages and other data from server at all times
        mythread = threading.Thread(target=self.controller.run)
        mythread.daemon = True
        mythread.start()

    """right clicking on user """
    def option_menu_event(self, event):
        print("selected someone")

    def selected_login_event(self, event):
        """Set as target currently selected login on login list"""
        target = self.logins_list.get(self.logins_list.curselection())
        self.controller.setTarget(target)
        self.target = target

    def send_entry_event(self, event):
        """Send message from entry field to target"""
        text = self.entry.get(1.0, tk.END)
        if text != '\n':
            if self.controller.getTarget() == None:
                self.controller.setTarget("all")
            message = 'GUI|msg|' + self.controller.getUsername() + '|' + self.controller.getTarget() + '|' + text[:-1]
            print(message)
            self.controller.sock.send(message.encode(ENCODING))
            self.entry.mark_set(tk.INSERT, 1.0)
            self.entry.delete(1.0, tk.END)
            self.entry.focus_set()
        else:
            messagebox.showinfo('Warning', 'You must enter non-empty message')

        with self.controller.lock:
            self.messages_list.configure(state='normal')
            if text != '\n':
                self.messages_list.insert(tk.END, text)
            self.messages_list.configure(state='disabled')
            self.messages_list.see(tk.END)

    def display_message(self, message):
        """Display message in ScrolledText widget"""
        with self.controller.lock:
            message = '< ' + self.controller.getUsername + '> ' + message
            self.messages_list.configure(state='normal')
            self.messages_list.insert(tk.END, message)
            self.messages_list.configure(state='disabled')
            self.messages_list.see(tk.END)


class LoginPage(tk.Frame):
    """ Login Page """

    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        tk.Frame.__init__(self, self.parent)
        self.email = None
        self.password = None

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
        # Email Entry field
        self.email = tk.Entry(self, width=20)
        self.email.insert(0, 'Email')
        self.email.focus_set()
        self.email.pack(side="top", fill="x")
        # Password Entry field
        self.password = tk.Entry(self, width=20, text='Password', show='*')
        self.password.insert(0, 'Password')
        self.password.pack(side="top", fill="x", pady=5)
        self.password.bind('<Return>', self.get_login_event)

        # Login Button
        loginBtn = tk.Button(self, text='Login', bg='#0084ff', activebackground='#0084ff', activeforeground='white', foreground='white', command=self.get_login_event)
        loginBtn.pack(side="top", fill="x")
        # Register Button
        registerBtn = tk.Button(self, text='Register', command=lambda: self.controller.show_frame("RegisterPage"))
        registerBtn.pack(side="top", fill="x")
        # Forgot button
        forgotBtn = tk.Button(self, text='Forgot Password', borderwidth=0, command=lambda: self.controller.show_frame("ForgotPassPage"))
        forgotBtn.pack(side="top", fill="x")
        # Copy right
        copy = tk.Label(self, text='PyChat © 2018', width=20)
        copy.pack(side="top", fill="x", pady=(100, 10))

    def get_login_event(self, event=None):
        """ Check login for correct info"""
        print('clicking login')
        # Get variables
        email = self.email.get()
        password = self.password.get()
        # Check file for both password and email
        print(email)
        print(password)
        if email.lower() == "email" or password.lower() == "password":
            display_alert("Please enter a value")
            return
        print('sending data to server')
        dataToSend = "GUI|login|" + email + "|" + password
        self.controller.sock.send(dataToSend.encode(ENCODING))
        print('sent data to server')
        # send error to user or to server
        data = self.controller.sock.recv(1024).decode(ENCODING)
        print('data: ' + data)
        # Call chatPage layout if server accepts connection
        if not "wrong password/username" in data:
            print('user: ' + data.split('|')[1] + ' has logged in')
            self.controller.setUsername(self.email.get())
            self.controller.show_frame("ChatPage")
        else:
            display_alert("Incorrect Email/Password")


class RegisterPage(tk.Frame):
    """ Registration Page"""

    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        tk.Frame.__init__(self, self.parent)

        self.name = None
        self.username = None
        self.email = None
        self.password = None

    def build(self):
        """ Build the registration page"""
        # Destroy previous versions of register page
        for widget in self.winfo_children():
            widget.destroy()

        self.parent.grid(row=0, column=0)

        load = Image.open('PyChat.png')
        render = ImageTk.PhotoImage(load)
        logo = tk.Label(self, image=render)
        logo.image = render
        logo.pack(side="top", fill="x", pady=20)
        # Full name of user
        self.name = tk.Entry(self, width=20)
        self.name.insert(0, 'Full name')
        self.name.focus_set()
        self.name.pack(side="top", fill="x", pady=5)
        # Username of user
        self.username = tk.Entry(self, width=20)
        self.username.insert(0, 'Username')
        self.username.focus_set()
        self.username.pack(side="top", fill="x", pady=5)
        # Email of user
        self.email = tk.Entry(self, width=20)
        self.email.insert(0, 'Email')
        self.email.focus_set()
        self.email.pack(side="top", fill="x", pady=5)
        # Password of user
        self.password = tk.Entry(self, width=20, text='Password', show='*')
        self.password.insert(0, 'Password')
        self.password.pack(side="top", fill="x", pady=5)
        self.password.bind('<Return>', self.get_register_event)

        # Register button
        registerBtn = tk.Button(self, text='Register', bg='#0084ff', activebackground='#0084ff', activeforeground='white', foreground='white', command=self.get_register_event)
        registerBtn.pack(side="top", fill="x")

        # Login button
        loginBtn = tk.Button(self, text='Login', command=lambda: self.controller.show_frame("LoginPage"))
        loginBtn.pack(side="top", fill="x")
        # Forgot button
        forgotBtn = tk.Button(self, text='Forgot Password', borderwidth=0,
                              command=lambda: self.controller.show_frame("ForgotPassPage"))
        forgotBtn.pack(side="top", fill="x", pady=10)
        # Copy right
        copy = tk.Label(self, text='PyChat © 2018', width=20)
        copy.pack(side="top", fill="x", pady=(90, 10))

    def get_register_event(self, event=None):
        """ Send register data """
        # Get variables
        name = self.name.get()
        username = self.username.get()
        email = self.email.get()
        password = self.password.get()
        # Check file for both password and email
        dataToSend = "GUI|register|" + name + "|" + username + "|" + email + "|" + password

        self.controller.sock.send(dataToSend.encode(ENCODING))

        # send error to user or to server
        data = self.controller.sock.recv(1024).decode(ENCODING)
        # Call chatPage layout if server accepts connection
        if "all" in str(data):
            """If registration is a success go to login page, then log the person in"""
            display_alert("Successfully registered, Please click login")
            self.controller.show_frame("LoginPage")
        else:
            print("data: " + data)
            display_alert(data.split('|')[1])


if __name__ == "__main__":
    app = PyChatApp()
    app.mainloop()
