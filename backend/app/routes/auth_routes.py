from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from app.models import User
from app.routes import bp

# Routes for user authentication
