# Python program to implement server side of chat room.
import socket
import select
import sys
from _thread import *

"""The first argument AF_INET is the address domain of the
socket. This is used when we have an Internet Domain with
any two hosts The second argument is the type of socket.
SOCK_STREAM means that data or characters are read in
a continuous flow."""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

"""
binds the server to an entered IP address and at the
specified port number.
The client must be aware of these parameters
"""
server.bind(("", 8080))

"""
listens for 100 active connections. This number can be
increased as per convenience.
"""
server.listen(100)

list_of_clients = []

# Give each file a variable
FRIENDSHIP = "friendship"
PENDING = "pending"
DM = "directMessage"
REGISTER = "registered"

class User:
    username = ""
    fullname = ""
    email = ""
    conn = ""


# display a help message to show what commands that the client can use to communicate with the server
def helpMenu(new_user):
    helpCmds = "List of possible commands:\n\t View friends \n\t Add Friend \n\t Remove Friend \n\t Direct Message / DM \n\t Boradcast \n\t Quit \n\t Help / --h "
    new_user.conn.send(helpCmds.encode())

def clientthread(new_user, addr):
    ''' Sends a message to the client who'S user is conn '''
    new_user.conn.send("Welcome to this chat room!".encode())

    while True:
        try:
            message = new_user.conn.recv(2048)
            if message:
                # Print message and user who sent it
                print("<" + addr[0] + "> " + message)
                # Calls broadcast function to send message to all
                message_to_send = "<" + addr[0] + "> " + message
                broadcast(message_to_send, new_user)
            else:
                # Remove connection from pool
                remove(new_user.conn)
        except:
            continue

def broadcast(message, new_user):
    ''' Broadcast a message to all connected clients '''
    for clients in list_of_clients:
        if clients != new_user.conn:
            try:
                clients.send(message.encode())
            except:
                clients.close()
                # if the link is broken, we remove the client
                remove(clients)

def checkFriends(new_user, usernameOfFriend):
    ''' Check if users are friends or not'''
    # Check if users are friends first
    viewF = viewFriends(new_user, usernameOfFriend)
    # Check if users have any pending requests
    viewP = searchPendingRequests(new_user, usernameOfFriend)
    # Logic
    if viewF:
        return True
    elif viewP:
        # The friendship has not been approved yet
        return False
    else:
        return False


def direct(message, new_user, usernameOfDirect):
    ''' Send a message to a user if you are friends with them'''
    # Check if users are friends
    if checkFriends(new_user, usernameOfDirect):
        # Users are friends
        for clients in list_of_clients:
            try:
                # Make sure we are only messaging the client/friend
                if clients.username == usernameOfDirect and clients.username != new_user.username:
                    clients.send(message.encode())
            except:
                clients.conn.close()
                remove(clients)
    else:
        new_user.conn.send("You are not friends with the user, you need to be in order to message them")


def remove(new_usern):
    ''' Remove client from pool of other clients'''
    if new_user in list_of_clients:
        list_of_clients.remove(new_user)

def addFriend(GLOBAL_VAR, friendReq):
    '''Add a friendship connection in pending.txt. In pending.txt, each line will show
       what users are requesting a friendship with what user  A,B    A is requesting a friendship with B.
       There will be no duplicates whereas B,A would be considered a duplicate to A,B '''
    #friendReq is the friend that is being requested to add as a friend

    file = open(GLOBAL_VAR, "r+")
    #check if the request has been made already / is still pending
    for line in file.readlines():
        li = line.split(";")
        for x in li:
            if x.contains(friendReq):
                return li

    # check if the users are already friends

    #if request hasnt been made or the users are not friends add a request to pending.txt

def viewFriends(user):
    '''Will show all of the friends with whom the client / requesting user,  is friends with'''
    friendsList = search_file(FRIENDSHIP, user.username)
    prepare = []
    i = 0
    if friendsList == []:
        prepare.append("You currently have no friends to display")
        return prepare
    else:
        s = ""
        if len(friendsList) > 1:
            s = "s"
        prepare.append("You have " + str(len(friendsList)) + " friend" + s)
    for friend in friendsList:
        i = i + 1
        prepare.append(str(i) + ": " + friend)
    return prepare

def viewFriends(new_user, usernameToSearch):
    ''' View friends for the user'''
    checkFriend = viewFriends(new_user.username)
    for name in checkFriend:
        if usernameToSearch == name:
            # Users are in fact friends
            return True
    return False

def viewPendingRequests(new_user):
    ''' View all my pending friend requests'''
    # Get all my pending friend requests
    pending = []
    view = search_file(PENDING, new_user.username)
    for line in view:
        f = line.split(';')
        if f[0] == new_user.username:
            pending.append(f[1])
        elif f[1] == new_user.username:
            pending.append(f[0])
    return pending

def searchPendingRequests(new_user, search):
    ''' Search all my pending requests for specific person'''
    view = viewPendingRequests(new_user)
    for line in view:
        if line == search:
            return True
    return False

def quit():
    '''returns quit if an error is thrown or if a user logs off'''
    return "quit"

"""Login allows usesr to login and start to use the functions of messageing and friendship manipulation"""
def login(new_user):
    tryAgain = True
    while tryAgain:
        fullName = ""
        email = ""
        # Get user input
        new_user.conn.send("Please enter username".encode())
        username = new_user.conn.recv(1024).decode()
        new_user.conn.send("Please enter password".encode())
        password = new_user.conn.recv(1024).decode()
        # Check the registration file
        try:
            f = open(REGISTER, 'r')
        except:
            f = open(REGISTER, 'w')
            f = open(REGISTER, 'r')
        exists = False
        # Read lines to see if user exists
        for line in f.readlines():
            if username in line and password in line:
                # User exists allow user to login
                exists = True
                username = line[0]
                email = line[1]
                fullName = line[2]
        f.close()
        # Tell the user to keep logging in
        if exists:
            tryAgain = False
            new_user.conn.send("Login successful".encode())
        else:
            tryAgain = True
            new_user.conn.send("Login information incorrect, please try again".encode())
    # Create user object
    new_user = User()
    new_user.username = username
    new_user.fullname = fullName
    new_user.email = email
    return True

def register(new_user):
    ''' Register a user'''
    tryAgain = True
    while tryAgain:
        # Sign up here
        new_user.conn.send("Please enter a username: ".encode())
        username = new_user.conn.recv(1024).decode()
        new_user.conn.send("Please enter a email:".encode())
        email = new_user.conn.recv(1024).decode()
        new_user.conn.send("What is your full name?".encode())
        fullName = new_user.conn.recv(1024).decode()
        new_user.conn.send("Please enter a password".encode())
        password = new_user.conn.recv(1024).decode()
        # Check data to make sure that it is not already in user
        userInUse = False
        # {username, email, fullname, password}
        userSearch = search_file(REGISTER, username)
        if userSearch != []:
            userInUse = True
            new_user.conn.send("username in use, try again".encode())
            continue
        # Check if user email is already in use
        userEmailSearch = search_file(REGISTER, email)
        if userEmailSearch != []:
            userInUse = True
            new_user.conn.send("email in use, try again".encode())
            continue
        # If everything is okay, lets save everything and append to file
        add_item(REGISTER, username+";"+email+";"+fullName+";"+password)
        new_user.conn.send("You are now registered, login now".encode())
        # Call login function
        login(new_user)
        return True

def loginOrRegister(new_user):
    ''' Ask the user if they want to login or register'''
    new_user.conn.send("Would you like to login or register? (0 = Login, 1= Register)".encode())
    choice = new_user.conn.recv(1024)
    if int(choice) is 1:
        register(new_user)
    else:
        login(new_user)
    return True

""" View current pending request for the currennt user, return true and a list the current pending requests"""
def viewRequests(search):
    f = []
    fp = open(PENDING, "r")
    # {"friendA: name, friendB: name2, date: 10-20} <-- A made the friend request
    for line in fp.readlines():
        li = line.split(';')
        if li[0] == search:
            f.append(li[1])
    return f

def search_file(GLOBAL_VAR, search):
    '''This function searches the DM.txt file for what the user is looking for. It does this by first going through a for loop that 
    reads all the lines and within doing that it uses the .split() function that allows it to read between the determinators'''
    f = []
    fp = open(GLOBAL_VAR, "r")
    for line in fp.readlines():
        li = line.split(';')
        for x in li:
            if x.contains(search):
                f.append(li)
    fp.close()
    return f
  
def add_item(GLOBAL_VAR, message):
    '''This function will add a message that the user enters, into the DM.txt file'''
    fp = open(GLOBAL_VAR, "a+")
    fp.write(message)
    fp.close()
            

while True:
    """Accepts a connection request and stores two parameters, 
    conn which is a socket object for that user, and addr 
    which contains the IP address of the client that just 
    connected"""
    conn, addr = server.accept()
    # Create a new user
    new_user = User()
    new_user.conn = conn
    # Pass that user into loginOrRegister
    loginOrRegister(new_user)

    #send message menu
    helpMenu(conn)

    """Maintains a list of clients for ease of broadcasting
    a message to all available people in the chatroom"""
    list_of_clients.append(conn)

    # prints the address of the user that just connected
    print(addr[0] + " connected")

    # creates and individual thread for every user
    # that connects
    start_new_thread(clientthread, (new_user, addr))

new_user.conn.close()
server.close()
