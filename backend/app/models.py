from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class PrivateChat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add fields for private chat

class GroupChat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add fields for group chat
