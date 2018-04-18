# Python program to implement server side of chat room.
import socket
import select
import sys
import time
from _thread import *
from Server_Helpers import *

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

while True:
    """Accepts a connection request and stores two parameters, 
    conn which is a socket object for that user, and addr 
    which contains the IP address of the client that just 
    connected"""
    try:
        time.sleep(5)
        print('about to accept')
        conn, addr = server.accept()
        # Create a new user
        print('creating new user')
        getGUI = None

        new_user = User()
        new_user.conn = conn

        # Pass that user into loginOrRegister
        data = conn.recv(1024)
        if data != "" and 'GUI' in data.decode(ENCODING):
            print('received something')
            data = data.decode(ENCODING)
            print("data: " + data)
            if 'GUI' in data:
                print(addr[0] + ' Connected via gui')
                #new_user.conn.send(data.encode(ENCODING))
                #print('sent info back to client')
                list_of_clients.append(conn)
                start_new_thread(clientthread, (new_user, addr, True))
        else:
            print(addr[0] + 'connected via terminal')
            loginOrRegister(new_user)
            print('send help menu')
            #send message menu
            helpMenu(conn)
            """Maintains a list of clients for ease of broadcasting
            a message to all available people in the chatroom"""
            list_of_clients.append(conn)

            # prints the address of the user that just connected
            print(addr[0] + " connected")

            # creates and individual thread for every user that connects
            start_new_thread(clientthread, (new_user, addr))
    except:
        print("There was some kind of error that happened")
#new_user.conn.close()
