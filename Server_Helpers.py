# Give each file a variable
FRIENDSHIP = "friendship.t"
PENDING = "pending.t"
DM = "directMessage.t"
REGISTER = "registered.t"

list_of_clients = []

ENCODING = 'utf-8'


class User:
    username = None
    fullname = None
    email = None
    password = None
    conn = None
    active = False
    dm = None  # Person who we are currently dming (if no one, then we are broadcasting)

def helpMenu(new_user):
    """ Display the help menu if a user gets stuck """
    helpCmds = "List of possible commands:\n\t View friends \n\t Add Friend \n\t Remove Friend \n\t Direct Message / DM \n\t Boradcast \n\t Quit \n\t Help / --h "
    new_user.conn.send(helpCmds.encode(ENCODING))


# Helper functions for processing data
def processLogin(self, data, connection):
    """ Helper to process login transactions """
    auth = login(self, True, data)
    message = data.split("|", 4)
    if "successful" in auth:
        # Update username in login list
        self.login_list[message[2]] = connection
        print(message[2] + ' has logged in')
        # Updating login list
        self.update_login_list()
    else:
        self.login_list[message[2]] = connection
        logins = 'login'
        logins += '|wrong password/username' + '\n'
        self.queue.put(('all', 'server', logins.encode(ENCODING)))


def processRegister(self, data, connection):
    """ Helper to process registration transactions"""
    auth = register(self, True, data)
    message = data.split("|")
    if "successful" in auth:
        # Update username in login list
        self.login_list[message[3]] = connection
        print(message[3] + ' has registered')
        # Updating login list
        self.update_login_list()
    else:
        self.login_list[message[3]] = connection
        logins = 'register'
        logins += '|' + auth + '\n'
        self.queue.put(('all', 'server', logins.encode(ENCODING)))


def processForgot(self, data, connection):
    """ Helper function to process password reset transactions"""
    auth = forgot(self, True, data)
    message = data.split("|")
    if "successful" in auth:
        # Update username in login list
        self.login_list[message[2]] = connection
        print(message[2] + ' has reset password')
        # Updating login list
        self.update_login_list()
    else:
        self.login_list[message[2]] = connection
        logins = 'forgot'
        logins += '|' + auth + '\n'
        self.queue.put(('all', 'server', logins.encode(ENCODING)))


def processLogout(self, data, connection):
    """ Helper to process logout transactions"""
    # Logs the user out
    message = data.split("|", 4)
    self.connection_list.remove(self.login_list[message[2]])
    if message[2] in self.login_list:
        del self.login_list[message[2]]
    print(message[2] + ' has logged out')
    self.update_login_list()


def processAddFriend(self, data, connection):
    """ Helper function to process adding friends """
    # GUI|addFriend|username|friendname
    auth = addFriend(data.split('|')[2], data.split('|')[3], True)
    message = data.split("|")
    if "successful" in auth:
        # Update username in login list
        self.login_list[message[2]] = connection
        print(message[2] + ' has sent a friend request')
        # Updating login list
        self.update_login_list()
    else:
        self.login_list[message[2]] = connection
        logins = 'addFriend'
        logins += '|' + auth + '\n'
        self.queue.put(('all', 'server', logins.encode(ENCODING)))


def processRemoveFreind(self, data, connection):
    """ Helper to remove friends"""
    # GUI|removeFriend|username|friendname
    auth = removeFriend(data.split('|')[2], data.split('|')[3], True)
    message = data.split("|")
    if "successful" in auth:
        # Update username in login list
        self.login_list[message[2]] = connection
        print(message[2] + ' has sent a friend request')
        # Updating login list
        self.update_login_list()
    else:
        self.login_list[message[2]] = connection
        logins = 'removeFriend'
        logins += '|' + auth + '\n'
        self.queue.put(('all', 'server', logins.encode(ENCODING)))


def processViewFriends(self, data, connection):
    """ Helper to view friends"""
    # GUI|viewFriends|username
    username = data.split('|')[2]
    auth = viewFriends(username)
    # print("auth processViewFriends: " + auth)
    message = data.split("|")
    if "successful" in auth:
        # Update username in login list
        self.login_list[message[2]] = connection
        print(message[2] + ' has sent a friend request')
        # Updating login list
        self.update_login_list()
    else:
        self.login_list[message[2]] = connection
        logins = 'GUI|viewFriends'
        logins += '|' + auth + '\n'
        self.queue.put(('all', 'server', logins.encode(ENCODING)))


def processViewSentRequests(self, data, connection):
    """ helper to view sent requests"""
    # GUI|viewSentRequests|username
    auth = viewSentPendingRequests(data.split('|')[2])
    message = data.split("|")
    if "successful" in auth:
        # Update username in login list
        self.login_list[message[2]] = connection
        print(message[2] + ' has sent a friend request')
        # Updating login list
        self.update_login_list()
    else:
        self.login_list[message[2]] = connection
        logins = 'viewSentRequests'
        logins += '|' + auth + '\n'
        self.queue.put(('all', 'server', logins.encode(ENCODING)))


def processViewPendingRequests(self, data, connection):
    """ Helper to view pending requests """
    # GUI|viewPendingRequests|username
    auth = viewPendingRequests(data.split('|')[2])
    message = data.split("|")
    if "successful" in auth:
        # Update username in login list
        self.login_list[message[2]] = connection
        print(message[2] + ' has sent a friend request')
        # Updating login list
        self.update_login_list()
    else:
        self.login_list[message[2]] = connection
        logins = 'viewPendingRequests'
        logins += '|' + auth + '\n'
        self.queue.put(('all', 'server', logins.encode(ENCODING)))

#def process(new_user, addr, usingGUI=False, data=None):
#    """ Sends a message to the client who'S user is conn """
#    # Handle GUI commands different from terminal
#    if usingGUI:
#        # Use a splitting method when sending the data through
#        # First param is what method we are going to do
#        method = data.split("|")[0]
#        print("method: " + method)
#
#        allData = data.split('|')
#        print('split this')
#        method = allData[1]
#        print('method: ' + method)
#
#        if method == 'login':
#            # GUI|login|username|password
#            login(new_user, True, data)
#        elif method == 'register':
#            # GUI|register|name|username|email|password
#            register(new_user, True, data)
#        elif method == "forgot":
#            # GUI|forgot|password
#            forgot(new_user, True, data)
#        elif method == "logout":
#            # GUI|logout
#            logout(new_user, list_of_clients)
#        elif method == 'checkUsername':
#            # GUI|checkUsername|username
#            checkUsername(data.split('|')[1])
#        elif method == 'checkEmail':
#            # GUI|checkEmail|email
#            checkEmail(data.split('|')[1])
#        elif method == 'msg':
#            # GUI|msg|message # Broadcast
#            # GUI|msg|user|message # Selected user
#            sendMessage(new_user, data.split('|')[2:])
#        elif method == 'addFriend':
#            # GUI|addFriend|target
#            addFriend(new_user, data, True)
#        elif method == 'removeFriend':
#            # GUI|removeFriend|target
#            removeFriend(new_user, data, True)
#        elif method == 'viewFriends':
#            # GUI|viewFriends
#            viewFriends(new_user, True)
#        elif method == 'viewSentRequests':
#            # GUI|viewSentRequests
#            viewSentPendingRequests(new_user)
#        elif method == 'viewRequests':
#            # GUI|viewRequests
#            viewRequests(new_user)
#        elif method == 'viewFriends':
#            # GUI|viewFriends
#            viewFriends(new_user)
#
#    else:
#       print('in terminal?')
#       try:
#           # Handle Terminal Commands
#           new_user.conn.send("Welcome to this chat room!".encode(ENCODING))
#           while True:
#               try:
#                   message = new_user.conn.recv(2048)
#                   if message:
#                       # Process the message that the user sent for commands
#                       if " " in message:
#                           msg = message.split(" ")
#                           if msg == "help" or msg == "-h":
#                               helpMenu(new_user)
#                               continue
#                           elif msg == "quit":
#                               quit()
#                               continue
#                           elif msg == "addfriend":
#                               if msg[1] == "":
#                                   new_user.conn.send("You must use the friends username to add them")
#                               addFriend(new_user, msg[1])
#                               continue
#                           elif msg == "removefriend":
#                               if msg[1] == "":
#                                   new_user.conn.send("You must use the friends username to remove them")
#                               removeFriend(new_user, msg[1])
#                               continue
#                           elif msg == "viewfriends":
#                               v = viewFriends(new_user)
#                               for x in v:
#                                   new_user.conn.send(str(x).encode(ENCODING))
#                                   continue
#                           elif msg == "direct":
#                               if msg[1] == "":
#                                   new_user.conn.send("You must use the friends username to direct them")
#                                   # Send friend a message that you want to direct them
#                                   new_user.conn.send("You are now in direct mode with " + msg[1])
#                                   # Send notification to friend
#                               continue
#                           elif msg == "broadcast":
#                               new_user.dm = ""
#                               new_user.conn.send("You are not in broadcast mode")
#                           else:
#                               sendMessage(new_user, message)
#                           sendMessage(new_user, message)
#                   else:
#                       # Remove connection from pool
#                       remove(new_user)
#               except:
#                   continue
#       except:
#           print("connection closed by client")
#           new_user.active = False
#           remove(new_user)

#def sendMessage(new_user, message):
#    """ Send Message """
#    # Print message and user who sent it
#    print("<" + new_user.username + "> " + message)
#    # Calls broadcast function to send message to all
#    message_to_send = "<" + new_user.username + "> " + message
#    broadcast(message_to_send, new_user)


#def remove(new_user):
#    """ Remove client from pool of other clients"""
#    if new_user in list_of_clients:
#        list_of_clients.remove(new_user)


# todo do we need this still?
#def broadcast(message, new_user):
#    """ Broadcast a message to all connected clients """
#
#    print("Broadcasting msg: " + message)
#
#    print('broadcasing message')
#    for clients in list_of_clients:
#        print('looping through clients')
#        if clients != new_user.conn:
#            try:
#                clients.send(message.encode(ENCODING))
#            except:
#                clients.close()
#                # if the link is broken, we remove the client
#                remove(clients)

# todo do we need this still?
#def direct(message, new_user):
#    """ Send a message to a user if you are friends with them"""
#    # Check if users are friends
#    if checkFriends(new_user, new_user.dm):
#        # Users are friends
#        for clients in list_of_clients:
#            try:
#                # Make sure we are only messaging the client/friend
#                if clients.username == new_user.dm and clients.username != new_user.username:
#                    clients.send(message.encode(ENCODING))
#            except:
#                clients.conn.close()
#                remove(clients)
#    else:
#        new_user.conn.send("You are not friends with the user, you need to be in order to message them")

def checkFriends(new_user, usernameOfFriend):
    """ Check if users are friends or not"""
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


def addFriend(new_user, friendReq, usingGUI=False):
    """Add a friendship connection in pending.txt. In pending.txt, each line will show
       what users are requesting a friendship with what user  A,B    A is requesting a friendship with B.
       There will be no duplicates whereas B,A would be considered a duplicate to A,B """
    # friendReq is the friend that is being requested to add as a friend
    viewP = searchPendingRequests(new_user, friendReq)
    if viewP != []:
        # You already sent a request to this user
        if usingGUI:
            return "REQUEST SENT"
        else:
            new_user.conn.send("You already sent a request to this user".encode(ENCODING))
        return False
    # Check if user sent request to me
    viewM = viewPendingRequests(new_user)
    if viewM != []:
        # User sent me a friend request, approve it
        add_item(FRIENDSHIP, new_user.username + "|" + friendReq)
        # Let the user know the friend request has been approved
        if usingGUI:
            return "FRIEND APPROVED"
        else:
            new_user.conn.send("Friend request approved".encode(ENCODING))
        return True
    # check if the users are already friends
    viewF = viewFriends(new_user)
    for line in viewF:
        if friendReq in line:
            if usingGUI:
                return "FRIENDS"
            else:
                new_user.conn.send("You are already friends".encode(ENCODING))
            return True
    # if request hasnt been made or the users are not friends add a request to pending.txt
    if viewP == [] and viewM == []:
        # Friend request has not been made yet, lets add it
        add_item(PENDING, new_user.username + "|" + friendReq)
        # Lets send a broadcast to the user to let them know about a new friend
        for clients in list_of_clients:
            # Loop through all the clients to find a username and send message to that connection
            if clients != friendReq:
                try:
                    clients.send(new_user.username + " sent you a friend request: type (approve/deny " + new_user.username + ")".encode(ENCODING))
                except:
                    new_user.conn.send("There was an error sending your friend request".encode(ENCODING))
                    return False
        if usingGUI:
            return "REQUEST SENT"
        else:
            new_user.conn.send("Friend request sent to " + friendReq)
        return True


def removeFriend(new_user, friend, usingGUI=False):
    """ Remove a person from pending or friendships"""
    remove_friend(FRIENDSHIP, new_user.username, friend)
    remove_friend(PENDING, new_user.username, friend)
    if usingGUI:
        return "FRIEND REMOVED"
    else:
        new_user.conn.send("You have removed " + friend.encode(ENCODING))
    return True


def viewFriends(current_user, usernameToSearch=None):
    """Will show all of the friends with whom the client / requesting user,  is friends with"""

    if usernameToSearch != None:

        checkFriend = viewFriends(current_user)
        for name in checkFriend:
            if usernameToSearch == name:
                # Users are in fact friends
                return True
        return False

    else:
        friendsList = search_file(FRIENDSHIP, current_user)
        listOfFriends = ''
        prepare = ""
        i = 0
        if friendsList == []:
            prepare = "You currently have no friends to display"
            return prepare
        else:
            s = ""
            if len(friendsList) > 1:
                s = "s"
            prepare += "You have " + str(len(friendsList)) + " friend" + s +"\n"

        for friend in friendsList:
            i = i + 1
            prepare += str(i) + ": " + str(friend)
           # listOfFriends += str(friend).split("|", 0)
        return prepare
        #return listOfFriends



def viewSentPendingRequests(username):
    """ View all requests i sent which are pending friend requests"""
    # Get all my pending friend requests
    pending = ""
    view = search_file(PENDING, username)
    for line in view:
        f = line.split('|')
        if f[0] == username:  # This is the person who sent the request
            pending += str((f[1])) + "\n"
    return pending


def viewPendingRequests(username):
    """ View all my pending friend requests"""
    # Get all my pending friend requests
    pending = ""
    view = search_file(PENDING, username)
    for line in view:
        f = line.split('|')
        if f[1] == username:  # This is the requestee
            pending += str((f[0])) + '\n'
    return pending


def searchPendingRequests(new_user, search):
    """ Search all my pending requests for specific person"""
    view = viewPendingRequests(new_user)
    for line in view:
        if line == search:
            return True
    return False


def login(new_user, usingGUI=False, data=None):
    """Login allows user to login and start to use the functions of mmessagingand friendship manipulation"""
    if usingGUI:
        exists = False
        print(data)
        # Get user and password
        fullName = None
        email = None
        username = data.split('|')[2]
        password = data.split('|')[3]
        # Check the registration file
        try:
            f = open(REGISTER, 'r')
        except:
            f = open(REGISTER, 'w')
        # Read lines to see if user exists
        try:
            for line in f.readlines():
                if username in line and password in line:
                    # User exists allow user to login
                    exists = True
                    username = line[0]
                    email = line[1]
                    fullName = line[2]
        except:
            return "You need to register first"
        f.close()
        if exists:
            # Create user object
            new_user.username = username
            new_user.fullname = fullName
            new_user.email = email
            new_user.active = True
            try:
                return "successful"
                #new_user.conn.send("LOGIN_SUCCESS".encode(ENCODING))
            except:
                print('There was an error for: ' + new_user.username)
        else:
            """ trying something different"""
            return "FAILED"
           #new_user.conn.send("Login information incorrect, please try again".encode(ENCODING))
    else:
        tryAgain = True
        while tryAgain:
            fullName = ""
            email = ""
            # Get user input
            new_user.conn.send("Please enter username".encode(ENCODING))
            username = new_user.conn.recv(1024).decode()
            new_user.conn.send("Please enter password".encode(ENCODING))
            password = new_user.conn.recv(1024).decode()
            # Check the registration file
            try:
                f = open(REGISTER, 'r')
            except:
                f = open(REGISTER, 'w')
            exists = False
            # Read lines to see if user exists
            for line in f.readlines():
                print('line: ' + line)
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
                new_user.conn.send("Login successful".encode(ENCODING))
            else:
                tryAgain = True
                new_user.conn.send("Login information incorrect, please try again".encode(ENCODING))
    return True


def logout(new_user, allUsersConnected):
    """ Logout """
    try:
        del allUsersConnected[new_user.username]
    except:
        print('could not remove user from list_of_clients')


def forgot(new_user, usingGUI=False, data=None):
    """ Forgot password """
    if usingGUI:
        # GUI|METHOD|EMAIL|PASSWORD
        email = data.split('|')[2]
        password = data.split('|')[3]
        userFound = search_file(REGISTER, email)
        #print('userfound: ' + str(userFound))
        if len(userFound) > 0:
            userFound = userFound[0]# Make sure its a string
            #print('userfound2: ' + str(userFound))
            # User found, lets change password (we should probably do this a different more secure way_
            # username + "|" + email + "|" + fullName + "|" + password
            username = userFound[0]
            email = userFound[1]
            name = userFound[2]
            remove_item(REGISTER, username + "|" + email + "|" + name)
            add_item(REGISTER, username + "|" + email + "|" + name + "|" + password)
            return "successful"
        else:
            return "Could not change password at this time"
    else:
        retry = True
        while retry:
            new_user.conn.send("Please enter your email address".encode(ENCODING))
            email = new_user.conn.recv(1024).decode(ENCODING)
            new_user.conn.send("Please enter a password".encode(ENCODING))
            password = new_user.conn.recv(1024).decode(ENCODING)
            new_user.conn.send("Re-enter your password again".encode(ENCODING))
            confirm = new_user.conn.recv(1024).decode(ENCODING)
            if password != confirm:
                new_user.conn.send("Passwords do not match, please try again".encode(ENCODING))
                retry = True
                continue
            if password == confirm:
                retry = False
            # Find user
            userFound = search_file(REGISTER, email)
            if len(userFound) > 0:
                userFound = userFound[0]  # Make sure its a string
                # User found, lets change password (we should probably do this a different more secure way_
                print(userFound)
                # username + "|" + email + "|" + fullName + "|" + password
                username = userFound.split('|')[0]
                email = userFound.split('|')[1]
                name = userFound.split('|')[2]
                remove_item(REGISTER, userFound)
                add_item(REGISTER, username + "|" + email + "|" + name + "|" + password)
                retry = False
                new_user.conn.send("Password has been changed successfully".encode(ENCODING))
            else:
                new_user.conn.send("Email is not associated with account".encode(ENCODING))
                retry = True


def checkUsername(username):
    """ Check if we can use a username"""
    if len(username) < 1 and not len(username) > 15 or '.' in username or '|' in username or ' ' in username or '|' in username:
        return False
    else:
        # Check file if user already exists
        infile = search_file(REGISTER, username)
        if len(infile) > 0:
            return False
        else:
            # Username is not in use
            return True


def checkEmail(email):
    """ Check if email is in use or valid"""
    if not '@' in email and not '.' in email:
        return False
    else:
        # Check file
        infile = search_file(REGISTER, email)
        if len(infile) > 0:
            return False
        else:
            # Email is not in use
            return True


def register(new_user, usingGUI=False, data=None):
    """ Register a user"""

    if usingGUI:
        # Get the user info from stream
        print(data)
        name = data.split('|')[2]
        username = data.split('|')[3]
        email = data.split('|')[4]
        password = data.split('|')[5]
        # Check the username
        check = checkUsername(username)
        if not check:
            return "Username cannot be used (a-z0-9)"
        # Check if email is in use
        check2 = checkEmail(email)
        if not check2:
            return "Email is in use or not valid"
        # Check password
        if len(password) < 6:
            return "password needs to be greater than 6 characters"
        # Allow registration
        # If everything is okay, lets save everything and append to file
        add_item(REGISTER, username + "|" + email + "|" + name + "|" + password+'\n')
        return "successful"
    else:
        tryAgain = True
        while tryAgain:
            # Sign up here
            usernameTryAagain = True
            while usernameTryAagain:
                new_user.conn.send("Please enter a username: ".encode(ENCODING))
                username = new_user.conn.recv(1024).decode()
                if len(username) > 5 and not '.' in username and not '|' in username and not ' ' in username:
                    usernameTryAagain = False
                else:
                    new_user.conn.send('username cannot contain  (.; ) and length must be greater than 5'.encode(ENCODING))

            emailTryAgain = True
            while emailTryAgain:
                new_user.conn.send("Please enter a email:".encode(ENCODING))
                email = new_user.conn.recv(1024).decode()
                if '@' in email and '.' in email:
                    emailTryAgain = False
                else:
                    new_user.conn.send('email is not valid, try again'.encode(ENCODING))

            new_user.conn.send("What is your full name?".encode(ENCODING))
            fullName = new_user.conn.recv(1024).decode()

            passwordTryAgain = True
            while passwordTryAgain:
                new_user.conn.send("Please enter a password".encode(ENCODING))
                password = new_user.conn.recv(1024).decode()
                new_user.conn.send("Please enter a password again".encode(ENCODING))
                password2 = new_user.conn.recv(1024).decode()
                if (len(password > 6) and password == password2):
                    passwordTryAgain = False
                if (len(password) < 6):
                    new_user.conn.send('password needs to be greater than 6 characters')

            # Check data to make sure that it is not already in user
            userInUse = False
            # {username, email, fullname, password}
            userSearch = search_file(REGISTER, username)
            if userSearch != []:
                userInUse = True
                new_user.conn.send("username in use, try again".encode(ENCODING))
                continue
            # Check if user email is already in use
            userEmailSearch = search_file(REGISTER, email)
            if userEmailSearch != []:
                userInUse = True
                new_user.conn.send("email in use, try again".encode(ENCODING))
                continue
            # If everything is okay, lets save everything and append to file
            add_item(REGISTER, username + "|" + email + "|" + fullName + "|" + password)
            new_user.conn.send("You are now registered, login now".encode(ENCODING))
            # Call login function
            login(new_user)
            return True



def loginOrRegister(new_user):
    """ Ask the user if they want to login or register"""
    new_user.conn.send("Would you like to login or register? (0 = Login, 1= Register)".encode(ENCODING))
    choice = eval(new_user.conn.recv(1024))
    if choice is 1:
        register(new_user)
    else:
        login(new_user)
    return True

def viewRequests(search):
    """View current pending request for the current user, return true and a list the current pending requests"""
    f = []
    fp = open(PENDING, "r")
    # {"friendA: name, friendB: name2, date: 10-20} <-- A made the friend request
    for line in fp.readlines():
        li = line.split('|')
        if li[0] == search:
            f.append(li[1])
    s = ""
    for st in f:
        s += "\n" + s
    return s  # Push a string instead of list for this

def search_file(GLOBAL_VAR, search):
    """This function first checks  searches the DM.txt file for what the user is looking for. It does this by first going through a for loop that
    reads all the lines and within doing that it uses the .split() function that allows it to read between the determinators"""
    """create file if does not already exist """
    try:
        fp = open(GLOBAL_VAR, 'r')
    except IOError:
        # If not exists, create the file
        fp = open(GLOBAL_VAR, 'w+').close()

    f = []
    try:
        for line in fp.readlines():
            li = line.split('|')
            for x in li:
                if x == search:
                    f.append(li)
    except:
        return []
    fp.close()
    return f

def remove_item(GLOBAL_VAR, search):
    """ Remove item from file"""
    f = open(GLOBAL_VAR, "r")
    lines = f.readlines()
    f.close()

    f = open(GLOBAL_VAR, "w")
    for line in lines:
        if search not in line:
            f.write(line)
    f.close()

def add_item(GLOBAL_VAR, message):
    """This function will add a message that the user enters, into the DM.txt file"""
    fp = open(GLOBAL_VAR, "a+")
    fp.write(message)
    fp.close()


def remove_friend(GLOBAL_VAR, personRemoving, personBeingRemoved):
    """ Remove a person from the friendship, pending"""
    f = open(GLOBAL_VAR, 'r')
    lines = f.readlines()
    f.close()
    f = open(GLOBAL_VAR, 'w')
    for line in lines:
        if not personBeingRemoved in line and not personRemoving in line:
            # Lets remove the person from the line by not adding them
            f.write(line)
    f.close()

    """ 
    Unread messages, will receive DM.txt the sender and receiver, it will be called when the user logs on 
    a message box will pop up saying how many messages they have and from whom.
    It will read through the file, find instances of the Direct messages between sender and target
    if the target has an unread message from the sender it will display those messages in the direct message window with 
    the sender. Once the message is read it will change the read receipt to true.
    DM.txt columns line Sender , target, time stamp, read receipt, content 
    returns an array of messages that have not been read by the user
    """


def unread_msg(GLOBAL_VAR, sender, target):
    unread = []
    result = ""

    fp = open(GLOBAL_VAR, "r")
    for line in fp.readlines():
        li = line.split('|')

        # split the line values into variables
        sndr = li[0]
        targ = li[1]
        time = li[2]
        receipt = li[3]
        content = li[4]

        if target == targ and sender == sndr and receipt == 0:
            unread.append(line)  # List of messages that have not been read

            # change the lines to be true
            li[3] = 1  # read receipt = true
            line = ", ".join(li)
            result += line + '\n'
            f = open(GLOBAL_VAR, 'w')  # should be in 'wt or 'w' mode
            f.write(result)
            f.close()

    fp.close()
    return unread
