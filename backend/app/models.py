from datetime import datetime
from flask_login import UserMixin
from app import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # Add more fields as needed

class PrivateChat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add fields for private chat

class GroupChat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add fields for group chat
