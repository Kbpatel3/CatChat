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


# User Authentication Routes
def authenticate_user(email, password):
    if email in emails:
        if passwords[email] == password:
            return True
    return False


@socketio.on('login')
def handle_login(data):
    email = data.get('email')
    password = data.get('password')

    # Authenticate user
    if authenticate_user(email, password):
        emit("login_response", {'success': True, 'message': 'Logged in successfully'})
    else:
        emit("login_response", {'success': False, 'message': 'Invalid credentials'})


@socketio.on('register')
def handle_register(data):
    print("Handling register request")
    email = data.get('email')
    password = data.get('password')

    # Check if the user already exists
    if email in emails:
        print("User already exists")
        emit("register_response", {'success': False, 'message': 'User already exists'})  # TODO Too much info?
    else:
        # Create a new user
        emails.append(email)
        passwords[email] = password
        emit("register_response", {'success': True, 'message': 'Account created successfully'})

    print(emails)
    print(passwords)


# Routes for chat



if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
