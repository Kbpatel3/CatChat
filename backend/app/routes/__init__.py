from flask import Blueprint
from . import auth_routes
from . import chat_routes

bp = Blueprint('main', __name__)

