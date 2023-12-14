from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from flask_socketio import join_room, leave_room, rooms
from flask_login import login_user
from flask import request, jsonify
from config import SECRET_KEY
import sqlite3
import stream_cipher
import crypto

# Initialize Flask
app = Flask(__name__)

# Set secret key for app
app.config['SECRET_KEY'] = SECRET_KEY

# Initialize CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Sample database
users = {}  # {user_id: {email: email, password: password}}
chats = {}  # {room_id: [{from_user_id: from_user_id, message: message}]}
emails = [] # [email]
passwords = {}  # {user_id: password}
connected_clients = []  # [user_id]
active_rooms = {}   # {user_id: [room_id]}
offline_messages = {}   # {user_id: [{from_user_id: from_user_id, message: message}]}
rooms_and_keys = {} # {room_id: key}



# Create a database for the users, chats, emails seperated, passwords seperated,
# connected clients, active rooms, and offline messages
# connect to the database
# conn = sqlite3.connect('database.db')
#
# # Create a cursor to execute SQL commands and queries
# cursor = conn.cursor()
#
# # Create a table for the users
# cursor.execute("CREATE TABLE users (user_id TEXT, email TEXT, password TEXT)")
#
# # Create a table for the chats
# cursor.execute("CREATE TABLE chats (room_id TEXT, from_user_id TEXT, message TEXT)")
#
# # Create a table for the emails
# cursor.execute("CREATE TABLE emails (email TEXT)")
#
# # Create a table for the passwords
# cursor.execute("CREATE TABLE passwords (user_id TEXT, password TEXT)")
#
# # Create a table for the connected clients
# cursor.execute("CREATE TABLE connected_clients (user_id TEXT)")
#
# # Create a table for the active rooms
# cursor.execute("CREATE TABLE active_rooms (user_id TEXT, room_id TEXT)")
#
# # Create a table for the offline messages
# cursor.execute("CREATE TABLE offline_messages (user_id TEXT, from_user_id TEXT, message TEXT)")



# TODO Base Connection Routes
@socketio.on('connection')
def handle_connection(user_id: str) -> None:
    """
    Handles the connection of a user to the server. Will create a new room for the user and join it.
    :param user_id: The user id of the user connecting to the server
    :return: None
    """
    print("Connection established")

    # Create a new room for the user and join it. The room name is passed as the user id
    if user_id not in connected_clients and user_id != "":
        join_room(user_id)

        # Add the user to the list of connected clients
        connected_clients.append(user_id)

    # Print the list of connected clients
    print(connected_clients)

    # # If the user has any pending messages, send them
    # if user_id in offline_messages:
    #     for message in offline_messages[user_id]:
    #         emit('privateMessage', {'from_user_id': message['from_user_id'], 'message': message['message']},
    #              room=user_id)
    #     del offline_messages[user_id]


@socketio.on('getConnectedClients')
def handle_get_connected_clients() -> None:
    """
    Handles a request for the list of connected clients
    :return: None
    """
    # Emit the list of connected clients to the front end
    emit('ConnectedClients', {'clients': connected_clients})


# TODO Room Routes
@socketio.on('createRoom')
def handle_room_creation(data: dict) -> None:
    """
    Handles the creation of a new room for a user
    :param data: The data passed from the client, which contains the client, the room name, and the user id
    :return: None
    """
    # Get the client, room name, and user id from the data
    client = data.get('client')
    room_id = data.get('roomName')
    user_id = data.get('userId')
    print("Creating room")

    # If the room does not exist, create it and join it
    if room_id not in active_rooms.values():
        # Join the room
        join_room(room_id)

        # Add client 1 to the list of active rooms
        if client not in active_rooms:
            active_rooms[client] = []

        # Add client 2 to the list of active rooms
        if user_id not in active_rooms:
            active_rooms[user_id] = []

        # The room id is the concatenation of the two user ids
        requester, receiver = room_id.split(".")
        variation1 = receiver + "." + requester
        variation2 = requester + "." + receiver

        # If the room id is the same as the variation, then that means the user is trying to create a room with themselves
        if variation1 == variation2 and variation1 not in active_rooms[client]:
            # Add the room to the list of active rooms for the client
            active_rooms[client].append(room_id)
            rooms_and_keys[room_id] = crypto.random.get_random_bytes(32)
            chats[room_id] = []

        # If the room id is not the same as the variation, then that means the user is trying to create a room with another user
        elif variation1 not in active_rooms[client] and variation1 not in active_rooms[user_id] and variation2 not in \
                active_rooms[client] and variation2 not in active_rooms[user_id]:
            # Add the room to the list of active rooms for the client and the other user
            active_rooms[client].append(room_id)
            active_rooms[user_id].append(room_id)
            rooms_and_keys[room_id] = crypto.random.get_random_bytes(32)
            chats[room_id] = []

    # Print the list of active rooms for the user
    print(active_rooms)

    # If the room has any pending messages, send them to the room
    if room_id in offline_messages:
        # Loop through the messages and send them to the room
        for message in offline_messages[room_id]:
            # SocketIO emits to the front end using the emit function. Passing the message data and the room id
            emit('privateMessage', {'from_user_id': message['from_user_id'], 'message': message['message']},
                 room=room_id)
        # Remove the room from the list of offline messages
        del offline_messages[room_id]


# TODO Message Routes
@socketio.on('privateMessage')
def handle_private_message(data: dict) -> None:
    """
    Handles a private message sent from one user to another
    :param data: The data passed from the front end, which contains the user id of the sender, the user id of the receiver, and the message
    :return:
    """
    to_user_id = data['to_user_id']
    from_user_id = data['from_user_id']
    message = data['message']

    # Check if the recipient is connected
    if to_user_id in connected_clients:
        # Emit to the front end using the emit function. Passing the sender, message, and room id
        emit('privateMessage', {'from_user_id': from_user_id, 'message': message}, room=to_user_id)
    else:
        # Recipient is not connected
        if to_user_id not in offline_messages:
            # Create a new list of offline messages for the recipient
            offline_messages[to_user_id] = []
        # Add the message to the list of offline messages for the recipient
        offline_messages[to_user_id].append({'from_user_id': from_user_id, 'message': message})


@socketio.on('newMessage')
def handle_new_message(data: dict) -> None:
    """
    Handles a new message sent from one user to another within a room
    :param data: The data passed from the front end, which contains the sender, receiver, and message
    :return: None
    """
    sender = data.get('sender')
    message = data.get('message')
    receiver = data.get('userId')
    print("New message received")
    print("Sender", sender)
    print("Receiver", receiver)
    print("Message", message)

    # If the sender and receiver are not empty
    if sender and receiver:
        # The room id is the concatenation of the sender and receiver
        room_id = sender + "." + receiver
        # The alternate room id is the concatenation of the receiver and sender
        alternate_room_id = receiver + "." + sender
        print("Appending onto the message history", room_id)

        # gets the secret key for the room
        key = rooms_and_keys[room_id]

        # If the room id is in the list of chats, append the message to the list of messages
        if room_id in chats:
            # Encrypted message and sender and then append encrypted data to the list of messages
            message_and_sender = encrypt_message(message, sender, key)
            encrypted_message = message_and_sender.split(".")[0]
            encrypted_sender = message_and_sender.split(".")[1]
            print("Encrypted message is:", encrypted_message)
            chats[room_id].append({'from_user_id': encrypted_sender, 'message': encrypted_message})

        # If the alternate room id is in the list of chats, append the message to the list of messages
        elif alternate_room_id in chats:
            # Encrypted message and sender and then append to the list of messages
            message_and_sender = encrypt_message(message, sender, key)
            encrypted_message = message_and_sender.split(".")[0]
            encrypted_sender = message_and_sender.split(".")[1]
            print("Encrypted message is:", encrypted_message)
            chats[alternate_room_id].append({'from_user_id': encrypted_sender, 'message': encrypted_message})


def encrypt_message(message: str, sender: str, key: str) -> str:
    cipher = stream_cipher.StreamCipher(key)
    encrypted_message = cipher.encrypt_string(message)
    encrypted_sender = cipher.encrypt_string(sender)
    return encrypted_message + "." + encrypted_sender


@socketio.on('getMessageHistory')
def handle_get_message_history(data: dict) -> None:
    """
    Handles a request for the message history of a room
    :param data: The data passed from the front end, which contains the sender and receiver
    :return: None
    """
    sender = data.get('sender')
    receiver = data.get('receiver')

    # If the sender and receiver are not empty
    if sender and receiver:
        # The room id is the concatenation of the sender and receiver
        room_id = sender + "." + receiver
        # The alternate room id is the concatenation of the receiver and sender
        alternate_room_id = receiver + "." + sender
        print("Getting message history for room", room_id)

        # If the room id is in the list of chats, emit the message history to the front end
        if room_id in chats:
            emit('messageHistory', {'messages': chats[room_id], 'room_key': rooms_and_keys[room_id]})

        # If the alternate room id is in the list of chats, emit the message history to the front end
        elif alternate_room_id in chats:
            emit('messageHistory', {'messages': chats[alternate_room_id], 'room_key': rooms_and_keys[alternate_room_id]})


# TODO User Authentication Routes
def authenticate_user(password: str, user_id: str) -> bool:
    """
    Authenticates the user by checking to see if the user exists in the database and if the password matches
    :param password : The password entered by the user
    :param user_id: The user id entered by the user
    :return: True if the user is authenticated, False otherwise
    """

    # Check if the user exists in the database
    if user_id in users:
        # Check if the password matches
        if users[user_id]['password'] == password:
            return True
    return False


@socketio.on('login')
def handle_login(data: dict) -> None:
    """
    Handles a login request from the front end
    :param data: The data passed from the front end, which contains the user id and password
    :return: None
    """
    print("Data for login", data)
    print(users)
    # Get the user id and password from the data
    user_id = data.get('userId')
    password = data.get('password')

    # Authenticate user
    if authenticate_user(password, user_id):
        # Send the front end a success message if the user is authenticated
        emit("login_response", {'success': True, 'message': 'Logged in successfully'})
    else:
        # Send the front end a failure message if the user is not authenticated
        emit("login_response", {'success': False, 'message': 'Invalid credentials'})


@socketio.on('register')
def handle_register(data: dict) -> None:
    """
    Handles a register request from the front end
    :param data: The data passed from the front end, which contains the email, user id, and password
    :return: None
    """
    print(data)
    print("Handling register request")
    # Get the email, user id, and password from the data
    email = data.get('email')
    user_id = data.get('userId')
    password = data.get('password')

    # Check if the email is already registered. If so, send the front end a failure message
    if email in emails:
        print("Email already registered")
        emit("register_response",
             {'success': False, 'message': 'An account already exists for this email'})  # TODO Too much info?

    # Check if the user id is already registered. If so, send the front end a failure message
    elif user_id in users:
        print("User already exists")
        emit("register_response",
             {'success': False, 'message': 'Username is already taken'})  # TODO Too much info?
    else:
        # Create a new user and add them to the database

        # Add the email to the list of emails
        emails.append(email)
        # Add the password for the user id to the list of passwords
        passwords[user_id] = password
        # Add the user to the database, user id holds the email and password
        users[user_id] = {'email': email, 'password': password}

        # Send the front end a success message
        emit("register_response", {'success': True, 'message': 'Account created successfully'})

    print(emails)
    print(passwords)
    print(users)


if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
