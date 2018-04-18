import socket
import select
import time

ENCODING = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(("127.0.0.1", 8080))

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

        read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])
        time.sleep(5)

        for socks in read_sockets:
            if socks == server:
                message = socks.recv(2048)
                print(message.decode(ENCODING))
            else:
                message = input()
                print("<You> " + message)
                server.send(message.encode(ENCODING))
    except:
        print('It seems that the server has closed connection')
        exit()