# Simple enough, just import everything from tkinter.
from tkinter import *
from bootstrap_py import *

# download and install pillow:
# http://www.lfd.uci.edu/~gohlke/pythonlibs/#pillow
from PIL import Image, ImageTk

# Here, we are creating our class, Window, and inheriting from the Frame
# class. Frame is a class from the tkinter module. (see Lib/tkinter/__init__)
class Window(Frame):

    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):
        # parameters that you want to send through the Frame class.
        Frame.__init__(self, master)

        # reference to the master widget, which is the tk window
        self.master = master

        # with that, we want to then run init_window, which doesn't yet exist
        self.init_window()

    # Creation of init_window
    def init_window(self):
        # changing the title of our master widget
        self.master.title("PyChat")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

<<<<<<< HEAD
        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # create the file object)
        file = Menu(menu)
        # create the file object)
        edit = Menu(menu)

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        file.add_command(label="Exit", command=self.client_exit)

        # added "file" to our menu
        menu.add_cascade(label="File", menu=file)
        # added "Edit" to our menu
        menu.add_cascade(label="Edit", menu=edit)



=======
>>>>>>> 4c95381d6e1aba53c65f489f507c39539ac75bbb
        load = Image.open("PyChat.png")
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img = Label(self, image=render)
        img.image = render
        img.place(x=30, y=10)

        title = Label(self, text="PyChat", font=("Arial Bold", 10))
        title.place(x=30, y=133)

        email = Entry(self, width=30)
        email.insert(0, 'Email')
        #global emailInput
        emailInput= email.get()
        email.place(x=5, y=160)

        password = Entry(self, show="*", width=30)
        password.insert(0, 'password')
        password.place(x=5, y=180)

        #login button will open the message window if login is success
        btn = Button(self, command = self.showMsgBox, width = 20, text = "Login")
        btn.place(x=20, y=210 )
        btn.grid

        title = Label(self, text="PyChat © 2018")
        title.place(x=50, y=380)

<<<<<<< HEAD
        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        edit.add_command(label="Show Img", command=self.showImg)
        edit.add_command(label="Show Text", command=self.showText)





    """if the login is a success show the message box GUI
        BUG: the login window needs to close when the message box opens"""

    def showMsgBox(self):
        msgBox = Toplevel(height = 400, width = 400)  #Create a new window
        msgBox.title("Message Box!")





    def showImg(self):
        load = Image.open("PyChat.png")
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)

    def showText(self):
        text = Label(self, text="Hey there good lookin!")
        text.pack()

=======
>>>>>>> 4c95381d6e1aba53c65f489f507c39539ac75bbb
    def client_exit(self):
        exit()


# root window created. Here, that would be the only window, but
# you can later have windows within windows.
root = Tk()
root.iconbitmap('pychat_2d5_icon.ico')
root.geometry("200x400")

# creation of an instance
app = Window(root)

# mainloop
root.mainloop()  