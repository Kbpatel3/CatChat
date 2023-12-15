import base64

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from flask_socketio import join_room, leave_room, rooms
from flask_login import login_user
from flask import request, jsonify
from config import SECRET_KEY
import stream_cipher
import Crypto.Random
import Crypto.Hash.SHA256
import database

# Initialize Flask
app = Flask(__name__)

# Set secret key for app
app.config['SECRET_KEY'] = SECRET_KEY

# Initialize CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

#Sample database
#users = {}  # {user_id: {email: email, password: password}}
chats = {}  # {room_id: [{from_user_id: from_user_id, message: message}]}
#emails = []  # [email]
#passwords = {}  # {user_id: password}
#connected_clients = []  # [user_id]
active_rooms = {}  # {user_id: [room_id]}
# rooms_and_keys = {}  # {room_id: key}

# Constants
SYM_KEY_LENGTH = 32
DIGEST_LENGTH = 64

# TODO Base Connection Routes
@socketio.on('connection')
def handle_connection(user_id: str) -> None:
    """
    Handles the connection of a user to the server. Will create a new room for the user and join it.
    :param user_id: The user id of the user connecting to the server
    :return: None
    """

    # Create a new room for the user and join it. The room name is passed as the user id
    if not database.get_connected_client(user_id) and user_id != "":
        join_room(user_id)

        # Add the user to the list of connected clients
        #connected_clients.append(user_id)

        # Add the user to the database
        database.add_connected_client(user_id)

    # Print the list of connected clients
    print("Connected clients", database.get_connected_clients())


@socketio.on('getConnectedClients')
def handle_get_connected_clients() -> None:
    """
    Handles a request for the list of connected clients
    :return: None
    """
    # Emit the list of connected clients to the front end
    connected_clients = database.get_connected_clients()
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
            #rooms_and_keys[room_id] = Crypto.Random.get_random_bytes(SYM_KEY_LENGTH)

            # Add the key to the rooms_and_keys database
            key = Crypto.Random.get_random_bytes(SYM_KEY_LENGTH)
            print("Key", key)
            database.add_room_and_key(room_id, key)

            chats[room_id] = []

        # If the room id is not the same as the variation, then that means the user is trying to create a room with another user
        elif variation1 not in active_rooms[client] and variation1 not in active_rooms[user_id] and variation2 not in \
                active_rooms[client] and variation2 not in active_rooms[user_id]:
            # Add the room to the list of active rooms for the client and the other user
            active_rooms[client].append(room_id)
            active_rooms[user_id].append(room_id)
            #rooms_and_keys[room_id] = Crypto.Random.get_random_bytes(SYM_KEY_LENGTH)

            # Add the key to the rooms_and_keys database
            key = Crypto.Random.get_random_bytes(SYM_KEY_LENGTH)
            print("Key", key)
            database.add_room_and_key(room_id, key)

            chats[room_id] = []

    # Print the list of active rooms for the user
    print(active_rooms)


# TODO Message Routes
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

    # If the sender and receiver are not empty
    if sender and receiver:
        # The room id is the concatenation of the sender and receiver
        room_id = sender + "." + receiver
        # The alternate room id is the concatenation of the receiver and sender
        alternate_room_id = receiver + "." + sender

        # If the room id is in the list of chats, append the message to the list of messages
        if room_id in chats:
            #key = rooms_and_keys[room_id]

            # Get the key from the database
            key = database.get_room_and_key(room_id)
            print("Key", key)

            # Encrypted message and sender and then append encrypted data to the list of messages
            hashed_message = hash_message(message)
            hashed_sender = hash_message(sender)

            combined_message = combine_message_and_hash(message, hashed_message)
            combined_sender = combine_message_and_hash(sender, hashed_sender)

            encrypted_message = encrypt(combined_message, key)
            encrypted_sender = encrypt(combined_sender, key)

            chats[room_id].append({'from_user_id': encrypted_sender, 'message': encrypted_message})

        # If the alternate room id is in the list of chats, append the message to the list of messages
        elif alternate_room_id in chats:
            #key = rooms_and_keys[alternate_room_id]

            # Get the key from the database
            key = database.get_room_and_key(alternate_room_id)

            # Encrypted message and sender and then append to the list of messages
            hashed_message = hash_message(message)
            hashed_sender = hash_message(sender)

            combined_message = combine_message_and_hash(message, hashed_message)
            combined_sender = combine_message_and_hash(sender, hashed_sender)

            encrypted_message = encrypt(combined_message, key)
            encrypted_sender = encrypt(combined_sender, key)

            chats[alternate_room_id].append({'from_user_id': encrypted_sender, 'message': encrypted_message})


def encrypt(data: str, key: bytes) -> bytes:
    """
    Encrypts the data using the key
    :param data: The data to be encrypted
    :param key: The key used to encrypt the data
    :return: The encrypted data
    """
    cipher = stream_cipher.StreamCipher(key)
    return cipher.encrypt(data.encode())


def decrypt(data: bytes, key: bytes) -> str:
    """
    Decrypts the data using the key
    :param data: The data to be decrypted
    :param key: The key used to decrypt the data
    :return: The decrypted data
    """
    cipher = stream_cipher.StreamCipher(key)
    return cipher.decrypt(data)


def hash_message(data: str) -> str:
    """
    Hashes the data using SHA256
    :param data: The data to be hashed
    :return: The hashed data
    """
    hashed_data = Crypto.Hash.SHA256.new(data.encode()).hexdigest()
    return hashed_data


def combine_message_and_hash(data: str, hashed_data) -> str:
    """
    Hashes the data using SHA256
    :param data: The data to be hashed
    :param hashed_data: The hashed data
    :return: The hashed data concatenated with the data
    """
    return data + hashed_data


def verify_hash(data: str, extracted_hash: str) -> bool:
    """
    Verifies the hash of the data using SHA256
    :param data: The data to be hashed
    :param extracted_hash: The hash to be verified
    :return: True if the hash is verified, False otherwise
    """
    hashed_data = hash_message(data)
    return hashed_data == extracted_hash.decode()


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

        # If the room id is in the list of chats, emit the message history to the front end
        if room_id in chats:
            decrypted_messages = decrypt_messages(room_id)
            emit('messageHistory', {'messages': decrypted_messages})

        # If the alternate room id is in the list of chats, emit the message history to the front end
        elif alternate_room_id in chats:
            decrypted_messages = decrypt_messages(alternate_room_id)
            emit('messageHistory', {'messages': decrypted_messages})


def decrypt_messages(room_id: str) -> list:
    # List of dictionaries
    messages = chats[room_id]

    #key = rooms_and_keys[room_id]

    # Get the key from the database
    key = database.get_room_and_key(room_id)

    # Return list of decrypted messages
    decrypted_messages = []

    for message in messages:
        # Decrypt the message and sender
        decrypted_message = decrypt(message['message'], key)
        decrypted_sender = decrypt(message['from_user_id'], key)

        # Split the decrypted parts into the data and hash
        extracted_message, extracted_message_hash = decrypted_message[:-DIGEST_LENGTH], decrypted_message[-DIGEST_LENGTH:]

        # Split the decrypted parts into the data and hash
        extracted_sender, extracted_sender_hash = decrypted_sender[:-DIGEST_LENGTH], decrypted_sender[-DIGEST_LENGTH:]

        # TODO Showcase the message integrity
        # extracted_message = b'I tampered with the message'

        # Verify the message integrity
        message_has_integrity = verify_hash(extracted_message.decode(), extracted_message_hash)

        # Verify the sender integrity
        sender_has_integrity = verify_hash(extracted_sender.decode(), extracted_sender_hash)

        if not message_has_integrity or not sender_has_integrity:
            decrypted_messages.append({'from_user_id': "Admin", 'message': "Message integrity compromised"})
        else:
            decrypted_messages.append(
            {'from_user_id': extracted_sender.decode(), 'message': extracted_message.decode()})

    return decrypted_messages


# TODO User Authentication Routes
def authenticate_user(password: str, user_id: str) -> bool:
    """
    Authenticates the user by checking to see if the user exists in the database and if the password matches
    :param password : The password entered by the user
    :param user_id: The user id entered by the user
    :return: True if the user is authenticated, False otherwise
    """

    # Get the user data from the database
    user_data = database.get_user(user_id)

    # Check if the user exists in the database
    if user_data and user_data[2] == password:
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

    user_data = database.get_user(user_id)

    # Check if the email is already registered. If so, send the front end a failure message
    if database.email_exists(email):
        print("Email already registered")
        emit("register_response",
             {'success': False, 'message': 'An account already exists for this email'})  # TODO Too much info?

    # Check if the user id is already registered. If so, send the front end a failure message
    elif user_data:
        print("User already exists")
        emit("register_response",
             {'success': False, 'message': 'Username is already taken'})  # TODO Too much info?
    else:
        # Create a new user and add them to the database

        # Add the email to the list of emails
        #emails.append(email)

        # Add the email to the database
        database.add_email(email)

        # Add the password for the user id to the list of passwords
        # TODO Salt and hash the password before adding it to the list of passwords

        #passwords[user_id] = password
        # Add the password to the database
        database.add_password(user_id, password)

        # Add the user to the database, user id holds the email and password
        #users[user_id] = {'email': email, 'password': password}

        # Add the user to the database with the email and password
        database.add_user(user_id, email, password)

        # Send the front end a success message
        emit("register_response", {'success': True, 'message': 'Account created successfully'})

    # Get all the emails from the database
    emails = database.get_emails()
    print(emails)


if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
