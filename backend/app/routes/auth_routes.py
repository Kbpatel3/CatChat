from flask import request, jsonify
from flask_login import login_user
from app.models import User
from app import app, db

# Routes for user authentication

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Validate data
    if 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Missing email or password'}), 400
    

    # Parse data
    email = data['email']
    password = data['password']

    print('email', email)
    print('password', password)

    # Query database for user
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        login_user(user)
        return jsonify({'success': 'Logged in successfully'}), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 400
    

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validate the request data
    if 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Invalid request'}), 400

    email = data['email']
    password = data['password']

    # Check if the user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'User already exists'}), 409

    # Create a new user
    new_user = User(email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Account created successfully'}), 201
