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
    new_user.conn.send(helpCmds.encode())

def clientthread(new_user, addr, usingGUI=False, data=None):
    """ Sends a message to the client who'S user is conn """
    # Handle GUI commands different from terminal
    if usingGUI:
        # Use a splitting method when sending the data through
        # First param is what method we are going to do
        method = data.split("|")[0]
        print("method: " + method)

        allData = data.split('|')
        print('split this')
        method = allData[1]
        print('method: ' + method)

        if method == 'login':
            print('logging you in')
            login(new_user, True)
        elif method == 'register':
            print('calling register')
            register(new_user, True)
        elif method == "forgot":
            print('forgot password')
            forgot(new_user, True)
        # TODO finish the messaging for GUI

        #new_user.conn.send("LOGIN_SUCCESS".encode(ENCODING))
        print('sent user a message that it was successful')
    else:
        print('in terminal?')
        try:
            # Handle Terminal Commands
            new_user.conn.send("Welcome to this chat room!".encode())
            while True:
                try:
                    message = new_user.conn.recv(2048)
                    if message:
                        # Process the message that the user sent for commands
                        if message.contains(" "):
                            msg = message.split(" ")
                            if msg == "help" or msg == "-h":
                                helpMenu(new_user)
                                continue
                            elif msg == "quit":
                                quit()
                                continue
                            elif msg == "addfriend":
                                if msg[1] == "":
                                    new_user.conn.send("You must use the friends username to add them")
                                addFriend(new_user, msg[1])
                                continue
                            elif msg == "removefriend":
                                if msg[1] == "":
                                    new_user.conn.send("You must use the friends username to remove them")
                                removeFriend(new_user, msg[1])
                                continue
                            elif msg == "viewfriends":
                                v = viewFriends(new_user)
                                for x in v:
                                    new_user.conn.send(str(x).encode())
                                    continue
                            elif msg == "direct":
                                if msg[1] == "":
                                    new_user.conn.send("You must use the friends username to direct them")
                                    # Send friend a message that you want to direct them
                                    new_user.conn.send("You are now in direct mode with " + msg[1])
                                    # Send notification to friend
                                continue
                            elif msg == "broadcast":
                                new_user.dm = ""
                                new_user.conn.send("You are not in broadcast mode")
                            else:
                                sendMessage(new_user, message)
                            sendMessage(new_user, message)
                    else:
                        # Remove connection from pool
                        remove(new_user)
                except:
                    continue
        except:
            print("connection closed by client")
            new_user.active = False
            remove(new_user)


def sendMessage(new_user, message):
    """ Send Message """
    # Print message and user who sent it
    print("<" + new_user.username + "> " + message)
    # Calls broadcast function to send message to all
    message_to_send = "<" + new_user.username + "> " + message
    broadcast(message_to_send, new_user)

def remove(new_user):
    """ Remove client from pool of other clients"""
    if new_user in list_of_clients:
        list_of_clients.remove(new_user)

def broadcast(message, new_user):
    """ Broadcast a message to all connected clients """
    for clients in list_of_clients:
        if clients != new_user.conn:
            try:
                clients.send(message.encode())
            except:
                clients.close()
                # if the link is broken, we remove the client
                remove(clients)

def direct(message, new_user):
    """ Send a message to a user if you are friends with them"""
    # Check if users are friends
    if checkFriends(new_user, new_user.dm):
        # Users are friends
        for clients in list_of_clients:
            try:
                # Make sure we are only messaging the client/friend
                if clients.username == new_user.dm and clients.username != new_user.username:
                    clients.send(message.encode())
            except:
                clients.conn.close()
                remove(clients)
    else:
        new_user.conn.send("You are not friends with the user, you need to be in order to message them")

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

def addFriend(new_user, friendReq):
    """Add a friendship connection in pending.txt. In pending.txt, each line will show
       what users are requesting a friendship with what user  A,B    A is requesting a friendship with B.
       There will be no duplicates whereas B,A would be considered a duplicate to A,B """
    # friendReq is the friend that is being requested to add as a friend
    viewP = searchPendingRequests(new_user, friendReq)
    if viewP != []:
        # You already sent a request to this user
        new_user.conn.send("You already sent a request to this user")
        return False
    # Check if user sent request to me
    viewM = viewPendingRequests(new_user)
    if viewM != []:
        # User sent me a friend request, approve it
        add_item(FRIENDSHIP, new_user.username + ";" + friendReq)
        # Let the user know the friend request has been approved
        new_user.conn.send("Friend request approved")
        return True
    # check if the users are already friends
    viewF = viewFriends(new_user)
    for line in viewF:
        if line.contains(friendReq):
            new_user.conn.send("You are already friends")
            return True
    # if request hasnt been made or the users are not friends add a request to pending.txt
    if viewP == [] and viewM == []:
        # Friend request has not been made yet, lets add it
        add_item(PENDING, new_user.username + ";" + friendReq)
        # Lets send a broadcast to the user to let them know about a new friend
        for clients in list_of_clients:
            # Loop through all the clients to find a username and send message to that connection
            if clients != friendReq:
                try:
                    clients.send(
                        new_user.username + " sent you a friend request: type (approve/deny " + new_user.username + ")".encode())
                except:
                    new_user.conn.send("There was an error sending your friend request")
                    return False
        new_user.conn.send("Friend request sent to " + friendReq)
        return True

def removeFriend(new_user, friend):
    """ Remove a person from pending or friendships"""
    remove_item(FRIENDSHIP, new_user.username, friend)
    remove_item(PENDING, new_user.username, friend)
    new_user.conn.send("You have removed " + friend.encode())
    return True

def viewFriends(user):
    """Will show all of the friends with whom the client / requesting user,  is friends with"""
    friendsList = search_file(FRIENDSHIP, user.username)
    prepare = []
    i = 0
    if friendsList == []:
        prepare.append("You currently have no friends to display")
        return prepare
    else:
        s = ""
        if len(friendsList) > 1:
            s = "s"
        prepare.append("You have " + str(len(friendsList)) + " friend" + s)
    for friend in friendsList:
        i = i + 1
        prepare.append(str(i) + ": " + friend)
    return prepare

def viewFriends(new_user, usernameToSearch):
    """ View friends for the user"""
    checkFriend = viewFriends(new_user.username)
    for name in checkFriend:
        if usernameToSearch == name:
            # Users are in fact friends
            return True
    return False


def viewSentPendingRequests(new_user):
    """ View all requests i sent which are pending friend requests"""
    # Get all my pending friend requests
    pending = []
    view = search_file(PENDING, new_user.username)
    for line in view:
        f = line.split(';')
        if f[0] == new_user.username:  # This is the person who sent the request
            pending.append(f[1])
    return pending


def viewPendingRequests(new_user):
    """ View all my pending friend requests"""
    # Get all my pending friend requests
    pending = []
    view = search_file(PENDING, new_user.username)
    for line in view:
        f = line.split(';')
        if f[1] == new_user.username:  # This is the requestee
            pending.append(f[0])
    return pending


def searchPendingRequests(new_user, search):
    """ Search all my pending requests for specific person"""
    view = viewPendingRequests(new_user)
    for line in view:
        if line == search:
            return True
    return False


def quit():
    """returns quit if an error is thrown or if a user logs off"""
    return "quit"


def login(new_user, usingGUI=False):
    """Login allows user to login and start to use the functions of mmessagingand friendship manipulation"""
    tryAgain = True
    while tryAgain:
        fullName = ""
        email = ""
        # Get user input
        if usingGUI:
            username = new_user.email
            password = new_user.password
        else:
            new_user.conn.send("Please enter username".encode())
            username = new_user.conn.recv(1024).decode()
            new_user.conn.send("Please enter password".encode())
            password = new_user.conn.recv(1024).decode()
            # Check the registration file
        try:
            f = open(REGISTER, 'r')
        except:
            f = open(REGISTER, 'w')
            f = open(REGISTER, 'r')
        exists = False
        # Read lines to see if user exists
        for line in f.readlines():
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
            if usingGUI:
                # Create user object
                new_user = User()
                new_user.username = username
                new_user.fullname = fullName
                new_user.email = email
                new_user.active = True

                new_user.conn.send("LOGIN_SUCCESS".encode(ENCODING))
            else:
                new_user.conn.send("Login successful".encode())
        else:
            if usingGUI:
                new_user.conn.send("Login information incorrect, please try again".encode(ENCODING))
            else:
                tryAgain = True
                new_user.conn.send("Login information incorrect, please try again".encode(ENCODING))
    return True

def forgot(new_user, usingGUI=False):
    """ Forgot password """
    if usingGUI:
        data = new_user.conn.recv(1024).decode(ENCODING)
        # GUI|METHOD|EMAIL|PASSWORD
        email = data.split('|')[1]
        password = data.split('|')[2]
        print('Email: ' + email)
        print('passing: ' + password)
        userFound = search_file(REGISTER, email)
        if userFound != "":
            userFound = userFound[0]# Make sure its a string
            # User found, lets change password (we should probably do this a different more secure way_
            print(userFound)
            # username + "|" + email + "|" + fullName + "|" + password
            username = userFound.split('|')[0]
            email = userFound.split('|')[1]
            name = userFound.split('|')[2]
            remove_item(REGISTER, userFound)
            add_item(REGISTER, username + "|" + email + "|" + name + "|" + password)
            return "SUCCESS_FORGOT_PASS"
        else:
            return "Could not change password at this time"
    else:
        # todo do the terminal version of this
        return "Could not change password for terminal type"

def register(new_user, usingGUI=False):
    """ Register a user"""
    tryAgain = True
    while tryAgain:
        # Sign up here
        usernameTryAagain = True
        while usernameTryAagain:
            new_user.conn.send("Please enter a username: ".encode())
            username = new_user.conn.recv(1024).decode()
            if len(username) > 5 and not username.contains('.') and not username.contains(
                    ';') and not username.contains(' '):
                usernameTryAagain = False
            else:
                new_user.conn.send('username cannot contain  (.; ) and length must be greater than 5'.encode())

        emailTryAgain = True
        while emailTryAgain:
            new_user.conn.send("Please enter a email:".encode())
            email = new_user.conn.recv(1024).decode()
            if email.contains('@') and email.contains('.'):
                emailTryAgain = False
            else:
                new_user.conn.send('email is not valid, try again'.encode())

        new_user.conn.send("What is your full name?".encode())
        fullName = new_user.conn.recv(1024).decode()

        passwordTryAgain = True
        while passwordTryAgain:
            new_user.conn.send("Please enter a password".encode())
            password = new_user.conn.recv(1024).decode()
            new_user.conn.send("Please enter a password again".encode())
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
            new_user.conn.send("username in use, try again".encode())
            continue
        # Check if user email is already in use
        userEmailSearch = search_file(REGISTER, email)
        if userEmailSearch != []:
            userInUse = True
            new_user.conn.send("email in use, try again".encode())
            continue
        # If everything is okay, lets save everything and append to file
        add_item(REGISTER, username + "|" + email + "|" + fullName + "|" + password)
        new_user.conn.send("You are now registered, login now".encode())
        # Call login function
        login(new_user)
        return True


def loginOrRegister(new_user):
    """ Ask the user if they want to login or register"""
    new_user.conn.send("Would you like to login or register? (0 = Login, 1= Register)".encode())
    choice = eval(new_user.conn.recv(1024))
    if choice is 1:
        register(new_user)
    else:
        login(new_user)
    return True


def viewRequests(search):
    """View current pending request for the currennt user, return true and a list the current pending requests"""
    f = []
    fp = open(PENDING, "r")
    # {"friendA: name, friendB: name2, date: 10-20} <-- A made the friend request
    for line in fp.readlines():
        li = line.split(';')
        if li[0] == search:
            f.append(li[1])
    return f


def search_file(GLOBAL_VAR, search):
    """This function searches the DM.txt file for what the user is looking for. It does this by first going through a for loop that
    reads all the lines and within doing that it uses the .split() function that allows it to read between the determinators"""
    f = []
    fp = open(GLOBAL_VAR, "r")
    for line in fp.readlines():
        li = line.split(';')
        for x in li:
            if x.contains(search):
                f.append(li)
    fp.close()
    return f

def remove_item(GLOBAL_VAR, search):
    """ Remove item from file"""
    fp = open(GLOBAL_VAR, "w")
    for line in fp.readlines():
        if line != search:
            fp.write(line)
    fp.close()

def add_item(GLOBAL_VAR, message):
    """This function will add a message that the user enters, into the DM.txt file"""
    fp = open(GLOBAL_VAR, "a+")
    fp.write(message)
    fp.close()


def remove_item(GLOBAL_VAR, personRemoving, personBeingRemoved):
    """ Remove a person from the friendship, pending"""
    f = open(GLOBAL_VAR, 'r')
    lines = f.readlines()
    f.close()
    f = open(GLOBAL_VAR, 'w')
    for line in lines:
        if not line.contains(personBeingRemoved) and not line.contains(personRemoving):
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
        li = line.split(';')

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
