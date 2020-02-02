# Flask app
import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Bootstrap(app)

from flask_sqlalchemy import SQLAlchemy

# Database
#if os.environ.get("HEROKU"):
#    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
#    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#else:
#    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///gtgapp.db"    
#    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#    app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

# Functionality
from application import views

from application.exercises import models
from application.exercises import views

from application.auth import models
from application.auth import views

# Authorization
from application.auth.models import User
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Create tables
try: 
    db.create_all()
except:
    pass