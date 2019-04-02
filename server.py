#!/usr/bin/env python3
"""
Flare Backend
 * Database handled by MongoDB, connection using PyMongo
 * User sessions, REST APIs with Flask and Flask-login
"""

from sys import exit
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, redirect, url_for, render_template, flash
from flask_login import LoginManager, login_manager, login_user, login_required

"""
Flask app and Flask-login manager
"""
app = Flask(__name__)
app.secret_key = 'The secret is out!'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "flare_login"

"""
Database functions
 * TODO: Create accounts with restrictive permissions, use those instead
"""

client = MongoClient('localhost', 27017)
flaredb = client.flaredb

def user_exists(username):
    return flaredb.accounts.count_documents({'userid': username}) > 0

def add_new_user(username, password):
    if user_exists(username):
        return
    password = generate_password_hash(password)
    flaredb.accounts.insert_one({'userid': username, 'password': password})

def authenticate(username, password):
    if not user_exists(username):
        return False
    stored = flaredb.accounts.find_one({'userid': username})
    print(stored)
    return check_password_hash(stored['password'], password)

class User:
    def __init__(self, name, password):
        self.name = name
        self.password = password
    def is_authenticated(self):
        return authenticate(self.name, self.password)
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.name


# Function below is used by flask-login
@login_manager.user_loader
def load_user(username):
    if not user_exists(username):
        return None
    stored = flaredb.accounts.find_one({'userid': username})
    return User(username, stored['password'])

@app.route("/index")
@app.route("/")
@login_required
def index():
    return render_template('panel.html')

@app.route("/panel")
@login_required
def panel():
    return render_template('panel.html')

@app.route("/login")
def flare_login():
    return render_template('login.html')

@app.route("/register")
def flare_register():
    return render_template('register.html', name='furlox')

@app.route("/login/user/", methods=['POST'])
def flare_login_user():
    username, password = request.form['username'], request.form['password']
    if authenticate(username, password):
        # This is a flask-login function which handles
        # user sessions
        login_user(User(username, password), remember=True)
        return redirect(url_for("index"))
    else:
        flash("Sorry! Invalid username/password. Please try again.")
        return redirect(url_for("flare_login"))

@app.route("/create/user/", methods=['POST'])
def flare_register_user():
    username, password = request.form['username'], request.form['password']
    if not username:
        flash("Sorry, username cannot be empty.")
        return redirect(url_for("flare_register"))
    if not password:
        flash("Sorry, password cannot be empty.")
        return redirect(url_for("flare_register"))
    if user_exists(username):
        flash("Sorry, that username is already taken.")
        return redirect(url_for("flare_register"))
    else:
        add_new_user(username, password)
        flash("You've been registered! Thanks!")
        return redirect(url_for("index"))

@app.route("/tracker")
@login_required
def flare_tracker():
    return render_template("tracker.html")
