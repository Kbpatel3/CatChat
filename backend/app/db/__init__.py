from flask_sqlalchemy import SQLAlchemy

# Create a SQLAlchemy object
db = SQLAlchemy()

# Import all models
from .models import User, PrivateChat, GroupChat


# Initialize the database
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()