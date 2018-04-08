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
        email.place(x=5, y=160)

        password = Entry(self, show="*", width=30)
        password.insert(0, 'password')
        password.place(x=5, y=180)

        btn = Button(self, text="Login", width=20)
        btn.place(x=20, y=210)

        title = Label(self, text="PyChat © 2018")
        title.place(x=50, y=380)

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