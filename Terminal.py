import socket
import select
import time
import queue
import threading

ENCODING = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(("localhost", 8080))

'''There are two possible input situations. Either the
      user wants to give  manual input to send to other people,
      or the server is sending a message  to be printed on the
      screen. Select returns from sockets_list, the stream that
      is reader for input. So for example, if the server wants
      to send a message, then the if condition will hold true
      below.If the user wants to send a message, the else
      condition will evaluate as true'''
while True:
    try:
        # maintains a list of possible input streams
        sockets_list = [socket.socket(), server]
        print("hello")
        read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])
        time.sleep(5)

        for socks in write_socket:
            print('socks: ')
            if socks == server:
                message = socks.recv(2048)
                print(message.decode(ENCODING))
            else:
                message = input('Enter a message: ')
                print("<You> " + message)
                server.send(message.encode(ENCODING))

        for socks in read_sockets:
            print('reading sockets')

        for socks in error_socket:
            print('error in socket')
    except:
        print('It seems that the server has closed connection')
