# Python program to implement server side of chat room.
from socket import *
from select import *
import sys
import time
from queue import *
from signal import *
from _thread import *
from Server_Helpers import *

"""The first argument AF_INET is the address domain of the
socket. This is used when we have an Internet Domain with
any two hosts The second argument is the type of socket.
SOCK_STREAM means that data or characters are read in
a continuous flow."""
server = socket(AF_INET, SOCK_STREAM)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

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

# todo fix this
while True:
    """Accepts a connection request and stores two parameters, 
    conn which is a socket object for that user, and addr 
    which contains the IP address of the client that just 
    connected"""
    print('looping')
    try:
        print('about to accept')
        conn, addr = server.accept()
        # Create a new user
        getGUI = None
        print('creating new user?')
        new_user = User()
        new_user.conn = conn
        list_of_clients.append(conn)

        while True:
            #time.sleep(5)
            # Pass that user into loginOrRegister
            data = conn.recv(1024)
            if data != "" and 'GUI' in data.decode(ENCODING):
                data = data.decode(ENCODING)
                if 'GUI' in data:
                    print(addr[0] + ' Connected via gui')

                    start_new_thread(clientthread, (new_user, addr, True, data)).start()
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
                start_new_thread(clientthread, (new_user, addr)).start()
    except:
        print("There was some kind of error that happened")
#new_user.conn.close()
