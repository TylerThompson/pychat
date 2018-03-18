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

def clientthread(conn, addr):
    ''' Sends a message to the client who'S user is conn '''
    conn.send("Welcome to this chatroom!".encode())

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

while True:
    """Accepts a connection request and stores two parameters, 
    conn which is a socket object for that user, and addr 
    which contains the IP address of the client that just 
    connected"""
    conn, addr = server.accept()

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
