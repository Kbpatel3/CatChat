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
connected_clients = {}
offline_messages = {}


# Base Routes
@socketio.on('joinRoom')
def handle_join_room(user_id):
    connected_clients[user_id] = request.sid
    join_room(user_id)

    # If the user has any pending messages, send them
    if user_id in offline_messages:
        for message in offline_messages[user_id]:
            emit('privateMessage', {'from_user_id': message['from_user_id'], 'message': message['message']},
                 room=request.sid)
        del offline_messages[user_id]


@socketio.on('privateMessage')
def handle_private_message(data):
    to_user_id = data['to_user_id']
    message = data['message']
    to_socket_id = connected_clients.get(to_user_id, None)

    if to_socket_id:
        emit('privateMessage', {'from_user_id': request.sid, 'message': message},
             room=to_socket_id)
    else:
        # Recipient is not connected
        if to_user_id not in offline_messages:
            offline_messages[to_user_id] = []

        offline_messages[to_user_id].append({'from_user_id': request.sid, 'message': message})


@socketio.on('disconnect')
def handle_disconnect():
    user_id = next(
        (user_id for user_id, socket_id in connected_clients.items() if socket_id == request.sid),
        None)
    if user_id:
        del connected_clients[user_id]


# User Authentication Routes
def authenticate_user(password, user_id):
    if user_id in users:
        if users[user_id]['password'] == password:
            return True
    return False


@socketio.on('login')
def handle_login(data):
    user_id = data.get('user_id')
    password = data.get('password')

    # Authenticate user
    if authenticate_user(password, user_id):
        emit("login_response", {'success': True, 'message': 'Logged in successfully'})
    else:
        emit("login_response", {'success': False, 'message': 'Invalid credentials'})


@socketio.on('register')
def handle_register(data):
    print("Handling register request")
    email = data.get('email')
    user_id = data.get('user_id')
    password = data.get('password')

    # Check if the user already exists
    if email in emails:
        print("User already exists")
        emit("register_response",
             {'success': False, 'message': 'User already exists'})  # TODO Too much info?

    elif user_id in users:
        print("User already exists")
        emit("register_response",
             {'success': False, 'message': 'Username is already taken'})  # TODO Too much info?
    else:
        # Create a new user
        emails.append(email)
        passwords[email] = password
        users[user_id] = {'email': email, 'password': password}
        emit("register_response", {'success': True, 'message': 'Account created successfully'})

    print(emails)
    print(passwords)
    print(users)


# Routes for chat


if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
