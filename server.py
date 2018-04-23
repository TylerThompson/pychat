# Python program to implement server side of chat room.
import time
import threading
import socket
import queue
from Server_Helpers import *

ENCODING = 'utf-8'
HOST = 'localhost'
PORT = 8080

class Server(threading.Thread):
    def __init__(self, host, port):
        super().__init__(daemon=False, target=self.run)

        self.host = host
        self.port = port
        self.buffer_size = 2048
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.connection_list = []
        self.login_list = {}
        self.queue = queue.Queue()

        self.shutdown = False
        try:
            self.sock.bind((str(self.host), int(self.port)))
            self.sock.listen(100)
            self.sock.setblocking(False)
        except socket.error:
            self.shutdown = True

        if not self.shutdown:
            listener = threading.Thread(target=self.listen, daemon=True)
            receiver = threading.Thread(target=self.receive, daemon=True)
            sender = threading.Thread(target=self.send, daemon=True)
            self.lock = threading.RLock()

            listener.start()
            receiver.start()
            sender.start()
            self.start()

    def run(self):
        """Main thread method"""
        print("Welcome to PyChat Server Admin Panel")
        print('You can do the following at anytime')
        print('"quit" to quit the server')
        print('"clients" to show list of active users')
        while not self.shutdown:
            message = input()
            if message == "quit":
                self.sock.close()
                self.shutdown = True
            elif message == 'clients':
                print('showing list of clients connected currently')
                if len(self.connection_list) == 0:
                    print('No one is currently connected on ' + str(socket.gethostbyname(socket.gethostname())) + ':' + str(self.port))
                for l in self.connection_list:
                    print(str(l))

    def listen(self):
        """Listen for new connections"""
        print('Initiated listener thread')
        while True:
            #print('listening for new connections')
            try:
                self.lock.acquire()
                connection, address = self.sock.accept()
                connection.setblocking(False)
                if connection not in self.connection_list:
                    self.connection_list.append(connection)
            except socket.error:
                pass
            finally:
                self.lock.release()
            time.sleep(0.050)

    def receive(self):
        """Listen for new messages"""
        print('Initiated receiver thread')
        while True:
            #print('listing for client activity')
            if len(self.connection_list) > 0:
                for connection in self.connection_list:
                    try:
                        self.lock.acquire()
                        data = connection.recv(self.buffer_size)
                    except socket.error:
                        data = None
                    finally:
                        self.lock.release()

                    self.process_data(data, connection)

    def send(self):
        """Send messages from server's queue"""
        print('Initiated sender thread')
        while True:
            if not self.queue.empty():
                target, origin, data = self.queue.get()
                if target == 'all':
                    self.broadcast(origin, data)
                else:
                    self.direct(target, data)
                self.queue.task_done()
            else:
                time.sleep(0.05)

    def broadcast(self, origin, data):
        """Send data to all users except origin"""
        if origin != 'server':
            print('origin: ' + origin)
            origin_address = self.login_list[origin]
            print('originAddre: ' + str(origin_address))
        else:
            origin_address = None

        print('connections: ' + str(len(self.connection_list)))

        for connection in self.connection_list:
            print(str(connection))
            if connection != origin_address:
                try:
                    self.lock.acquire()
                    print('datA: ' + str(data))
                    connection.send(data)
                except socket.error:
                    self.remove_connection(connection)
                finally:
                    self.lock.release()

    def direct(self, target, data):
        """Send data to specified target"""
        try:
            target_address = self.login_list[target]
            try:
                self.lock.acquire()
                target_address.send(data)
            except socket.error:
                self.remove_connection(target_address)
            finally:
                self.lock.release()
        except socket.error:
            self.lock.release()


    def process_data(self, data, connection):
        #print('processing data')
        """Process received data"""
        if data:
            message = data.decode(ENCODING)
            decodedData = message
            print('message data: ' + message)
            message = message.split("|", 4)

            try:
                method = message[1]
            except IndexError:
                method = message[0]

            if method == 'login':
                processLogin(self, decodedData, connection)
            elif method == 'register':
                processRegister(self, decodedData, connection)
            elif method == 'logout':
                processLogout(self, decodedData, connection)
            elif method == 'forgot':
                processForgot(self, decodedData, connection)
            elif method == 'msg' and message[3] != 'all':
                # Sends message to specific person so they can only see the message
                msg = data.decode(ENCODING) + '\n'
                data = msg.encode(ENCODING)
                self.queue.put((message[3], message[1], data))
            elif method == 'msg':
                # Sends message to everyone connected
                msg = data.decode(ENCODING) + '\n'
                data = msg.encode(ENCODING)
                self.queue.put(('all', message[2], data))
            elif method == 'update_login_list':
                self.update_login_list()
            elif method == 'addFriend':
                processAddFriend(self, decodedData, connection)
            elif method == 'removeFriend':
                processRemoveFreind(self, decodedData, connection)
            elif method == 'viewFriends':
                processViewFriends(self, decodedData, connection)
            elif method == 'viewSentRequests':
                processViewSentRequests(self, decodedData, connection)
            elif method == 'viewPendingRequests':
                processViewPendingRequests(self, decodedData, connection)

# TODO put these in helper functions
    def remove_connection(self, connection):
        print('removing connection')
        """Remove connection from server's connection list"""
        self.connection_list.remove(connection)
        for login, address in self.login_list.items():
            if address == connection:
                del self.login_list[login]
                break
        self.update_login_list()

# TODO put these in helper functions
    def update_login_list(self):
        print('updating login list')
        """Update list of active users"""
        logins = 'GUI|login_list|'
        i = 0
        for login in self.login_list:
            if i == 0:
                logins += login
            else:
                logins += ';' + login
            i = i+1
        logins += ';all' + '\n'
        self.queue.put(('all', 'server', logins.encode(ENCODING)))

# Create new server with (IP, port)
if __name__ == '__main__':
    server = Server(HOST, PORT)
