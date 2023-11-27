from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from config import SECRET_KEY

# Initialize Flask
app = Flask(__name__)

# Set secret key for app
app.config['SECRET_KEY'] = SECRET_KEY

# Initialize CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")


# Routes
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('join')
def handle_join(data):
    room = data['room']
    join_room(room)
    print(f'User {data["user"]} joined room {room}')

@socketio.on('leave')
def handle_leave(data):
    room = data['room']
    leave_room(room)
    print(f'User {data["user"]} left room {room}')

@socketio.on('message')
def handle_message(data):
    room = data['room']
    send(data['message'], room=room, broadcast=True)
    print(f'Message from {data["user"]} in room {room}: {data["message"]}')

@socketio.on('private_message')
def handle_private_message(data):
    recipient = data['recipient']
    message = data['message']
    emit('private_message', {'user': data['user'], 'message': message}, room=recipient)
    print(f'Private message from {data["user"]} to {recipient}: {message}')

@socketio.on('typing')
def handle_typing(data):
    room = data['room']
    emit('typing', {'user': data['user']}, room=room)

@socketio.on('get_users')
def handle_get_users(data):
    room = data['room']
    users = list(get_room_users(room))
    emit('user_list', {'users': users}, room=room)


if __name__ == '__main__':
    socketio.run(app, debug=True, port=5005)
