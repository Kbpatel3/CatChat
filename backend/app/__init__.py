from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS

app = Flask(__name__)

import routes
from db import init_db

CORS(app)
app.config.from_object('config.Config')
init_db(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
