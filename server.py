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


# Give each file a variable
friendship = "friendship"
pending = "pending"
dm = "directMessage"
registered = "registered"



# display a help message to show what commands that the client can use to communicate with the server
def helpMenu(conn):
    helpCmds = "List of possible comands:\n \t View friends \n \t Add Friend \n \t Remove Friend \n \t Direct Message / DM \n \t Boradcast \n \t Quit \n \t Help / --h "
    conn.send(helpCmds.encode())



list_of_clients = []

def clientthread(conn, addr):
    ''' Sends a message to the client who'S user is conn '''
    conn.send("Welcome to this chat room!".encode())

    while True:
        try:
            message = conn.recv(2048)
            if message:
                # Print message and user who sent it
                print("<" + addr[0] + "> " + message)
                # Calls broadcast function to send message to all
                message_to_send = "<" + addr[0] + "> " + message
                broadcast(message_to_send, conn)
            else:
                # Remove connection from pool
                remove(conn)
        except:
            continue

def broadcast(message, connection):
    ''' Broadcast a message to all connected clients '''
    for clients in list_of_clients:
        if clients != connection:
            try:
                clients.send(message.encode())
            except:
                clients.close()
                # if the link is broken, we remove the client
                remove(clients)

def remove(connection):
    ''' Remove client from pool of other clients'''
    if connection in list_of_clients:
        list_of_clients.remove(connection)

""" Add a friendship connection in pending.txt. In pending.txt, each line will show 
    what users are requesting a friendship with what user  A,B    A is requesting a friendship with B.
    There will be no duplicates whereas B,A would be considered a duplicate to A,B 
    
    will call viewFriends() and viewRequests()"""

def addFriend(GLOBAL_VAR, friendReq):
    #friendReq is the friend that is being requested to add as a friend

    file = open(GLOBAL_VAR, "r+")
    #check if the request has been made already / is still pending
    for line in file.readline():
        li = line.split(";")
        for x in li:
            if x.contains(friendReq):
                return li


    # check if the users are already friends


    #if request hasnt been made or the users are not friends add a request to pending.txt


""" Will show all of the friends with whom the client / requesting user,  is friends with"""
def viewFriends():


    return

""" returns quit if an error is thrown or if a user logs off"""
def quit():

    return quit()

"""Login allows usesr to login and start to use the functions of messageing and friendship manipulation"""
def login():

    return

""" View current pending request for the currennt user, return true and a list the current pending requests"""
def viewRequests(GLOBAL_VAR, search):
    fp = open(GLOBAL_VAR, "r")
    for line in fp.readlines():
        li = line.split(';')
        for x in li:
            if x.contains(search):
                return li
    return

def search_file(GLOBAL_VAR, search):
    '''This function searches the DM.txt file for what the user is looking for. It does this by first going through a for loop that 
    reads all the lines and within doing that it uses the .split() function that allows it to read between the determinators'''
    fp = open(GLOBAL_VAR, "r")
    for line in fp.readlines():
        li = line.split(';')
        for x in li:
            if x.contains(search):
                return li
    fp.close() 
  
def add_item(GLOBAL_VAR, message):
    '''This function will add a message that the user enters, into the DM.txt file
    fp = open(GLOBAL_VAR, "a+")
    fp.write(message)
    fp.close()
            

while True:
    """Accepts a connection request and stores two parameters, 
    conn which is a socket object for that user, and addr 
    which contains the IP address of the client that just 
    connected"""
    conn, addr = server.accept()



    #send message menu
    helpMenu(conn)

    """Maintains a list of clients for ease of broadcasting
    a message to all available people in the chatroom"""
    list_of_clients.append(conn)

    # prints the address of the user that just connected
    print(addr[0] + " connected")

    # creates and individual thread for every user
    # that connects
    start_new_thread(clientthread, (conn, addr))

conn.close()
server.close()
