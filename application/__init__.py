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

from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager, current_user
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality"

from functools import wraps

def login_required(_func=None, *, role="ANY"):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not (current_user and current_user.is_authenticated):
                return login_manager.unauthorized()

            acceptable_roles = set(("ANY", *current_user.roles()))

            if role not in acceptable_roles:
                return login_manager.unauthorized()

            return func(*args, **kwargs)
        return decorated_view
    return wrapper if _func is None else wrapper(_func)

# Functionality
from application import views

from application.exercises import models
from application.exercises import views

from application.auth import models
from application.auth import views

# Authorization
from application.auth.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Create tables
try: 
    db.create_all()
except:
    pass