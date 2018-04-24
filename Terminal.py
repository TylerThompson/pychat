import socket
import select
import time
import queue
import threading

ENCODING = 'utf-8'

'''There are two possible input situations. Either the
      user wants to give  manual input to send to other people,
      or the server is sending a message  to be printed on the
      screen. Select returns from sockets_list, the stream that
      is reader for input. So for example, if the server wants
      to send a message, then the if condition will hold true
      below.If the user wants to send a message, the else
      condition will evaluate as true'''
from socket import *
from time import sleep

# Create a socket and connect to the server
serverName = "127.0.0.1"  # Use IP address of server
serverPort = 8080
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# Sign up or login
while 1:
    try:
        # Listen to response from server and respond to it
        response = clientSocket.recv(1024).decode(ENCODING)
        if "Error" in response or "Successful" in response:
            # Print out any error or congrats messages
            print(response)
        else:
            # Allow for user to input any responses needed
            request = input(response)
            if "quit" in request:
                # Allow for user to quit at anytime
                clientSocket.close()
                exit()
            # Send information to the server
            clientSocket.send(request.encode(ENCODING))
            sleep(1)
            request = ''
    except:
        # Let user know if there are any issues with processing requests
        print("There was an error")
        # Close socket if major error occurs (server disconnecting)
        clientSocket.close()
        exit()
