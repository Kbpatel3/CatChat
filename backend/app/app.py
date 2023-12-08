from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from flask_socketio import join_room, leave_room, rooms
from flask_login import login_user
from flask import request, jsonify
from config import SECRET_KEY

# Initialize Flask
app = Flask(__name__)

# Set secret key for app
app.config['SECRET_KEY'] = SECRET_KEY

# Initialize CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Sample database
users = {}
chats = {}
emails = []
passwords = {}
connected_clients = []
active_rooms = {}
offline_messages = {}


# Base Routes
@socketio.on('connection')
def handle_connection(user_id):
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


@socketio.on('createRoom')
def handle_room_creation(data):
    client = data.get('client')
    room_id = data.get('roomName')
    user_id = data.get('userId')
    print("Creating room")

    # Create a new room for the user and join it. The room name is passed as the user id
    if room_id not in active_rooms.values():
        join_room(room_id)

        # Add the user to the list of active rooms for the user
        if client not in active_rooms:
            active_rooms[client] = []

        if user_id not in active_rooms:
            active_rooms[user_id] = []

        requester, receiver = room_id.split(".")
        variation1 = receiver + "." + requester
        variation2 = requester + "." + receiver

        if variation1 == variation2 and variation1 not in active_rooms[client]:
            active_rooms[client].append(room_id)

        elif variation1 not in active_rooms[client] and variation1 not in active_rooms[user_id] and variation2 not in active_rooms[client] and variation2 not in active_rooms[user_id]:
            active_rooms[client].append(room_id)
            active_rooms[user_id].append(room_id)

    # Print the list of active rooms for the user
    print(active_rooms)

    # If the user has any pending messages, send them
    if room_id in offline_messages:
        for message in offline_messages[room_id]:
            emit('privateMessage', {'from_user_id': message['from_user_id'], 'message': message['message']},
                 room=room_id)
        del offline_messages[room_id]


@socketio.on('privateMessage')
def handle_private_message(data):
    to_user_id = data['to_user_id']
    from_user_id = data['from_user_id']
    message = data['message']

    if to_user_id in connected_clients:
        # Emit to room to_user_id
        emit('privateMessage', {'from_user_id': from_user_id, 'message': message}, room=to_user_id)
    else:
        # Recipient is not connected
        if to_user_id not in offline_messages:
            offline_messages[to_user_id] = []

        offline_messages[to_user_id].append({'from_user_id': from_user_id, 'message': message})


@socketio.on('newMessage')
def handle_new_message(data):
    sender = data.get('sender')
    message = data.get('message')
    receiver = data.get('userId')
    print("New message received")
    print("Sender", sender)
    print("Receiver", receiver)
    print("Message", message)
    if sender and receiver:
        room_id = sender + "." + receiver
        alternate_room_id = receiver + "." + sender
        print("Appending onto the message history", room_id)

        if room_id in chats:
            chats[room_id].append({'from_user_id': sender, 'message': message})

        elif alternate_room_id in chats:
            chats[alternate_room_id].append({'from_user_id': sender, 'message': message})

        try:
            print(type(room_id))
            print(chats[room_id])
        except:
            print(type(alternate_room_id))
            print(chats[alternate_room_id])



@socketio.on('getMessageHistory')
def handle_get_message_history(data):
    sender = data.get('sender')
    receiver = data.get('receiver')

    if sender and receiver:
        room_id = sender + "." + receiver
        alternate_room_id = receiver + "." + sender
        print("Getting message history for room", room_id)

        if room_id in chats:
            emit('messageHistory', {'messages': chats[room_id]})

        elif alternate_room_id in chats:
            emit('messageHistory', {'messages': [{'from_user_id': 'admin', 'message': 'No messages yet'}]})

@socketio.on('getConnectedClients')
def handle_get_connected_clients():
    emit('ConnectedClients', {'clients': connected_clients})


# @socketio.on('disconnect')
# def handle_disconnect():
#     user_id = next(
#         (user_id for user_id, socket_id in connected_clients.items() if socket_id == request.sid),
#         None)
#     if user_id:
#         del connected_clients[user_id]


# User Authentication Routes
def authenticate_user(password, user_id):
    if user_id in users:
        if users[user_id]['password'] == password:
            return True
    return False


@socketio.on('login')
def handle_login(data):
    print("Data for login", data)
    print(users)
    user_id = data.get('userId')
    password = data.get('password')

    # Authenticate user
    if authenticate_user(password, user_id):
        emit("login_response", {'success': True, 'message': 'Logged in successfully'})
    else:
        emit("login_response", {'success': False, 'message': 'Invalid credentials'})


@socketio.on('register')
def handle_register(data):
    print(data)
    print("Handling register request")
    email = data.get('email')
    user_id = data.get('userId')
    password = data.get('password')

    # Check if the user already exists
    if email in emails:
        print("Email already registered")
        emit("register_response",
             {'success': False, 'message': 'An account already exists for this email'})  # TODO Too much info?
    elif user_id in users:
        print("User already exists")
        emit("register_response",
             {'success': False, 'message': 'Username is already taken'})  # TODO Too much info?
    else:
        # Create a new user
        emails.append(email)
        passwords[user_id] = password
        users[user_id] = {'email': email, 'password': password}
        emit("register_response", {'success': True, 'message': 'Account created successfully'})

    print(emails)
    print(passwords)
    print(users)


# Routes for chat


if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
