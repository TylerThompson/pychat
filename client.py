# Python program to implement client side of chat room.
import socket
import select
import sys
import gui


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(("localhost", 8080))
#server.connect(("172.122.144.137", 8080))




while True:

    # maintains a list of possible input streams
    sockets_list = [socket.socket(), server]

    #userEmail = gui.ge

    '''There are two possible input situations. Either the
    user wants to give  manual input to send to other people,
    or the server is sending a message  to be printed on the
    screen. Select returns from sockets_list, the stream that
    is reader for input. So for example, if the server wants
    to send a message, then the if condition will hold true
    below.If the user wants to send a message, the else
    condition will evaluate as true'''
    read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])

    print("Type help or --h for command menu.")

    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048)
            if message == "quit":
                server.close()
                quit()
            print(message.decode())
        else:
            message = sys.stdin.readline()
            server.send(message.encode())
            sys.stdout.write("<You>")
            sys.stdout.write(message)
            sys.stdout.flush()
server.close()