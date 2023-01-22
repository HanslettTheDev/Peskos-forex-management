import os
from flask import Flask, flash, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_bcrypt import Bcrypt
from flask_seeder import FlaskSeeder
from functools import wraps
from peskos.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
seeder = FlaskSeeder()
login_manager.login_view = "must_login.login"
login_manager.login_message_category = "info"

path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'db.sqlite')

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    seeder.init_app(app, db)
    
    if not os.path.exists(path):
        with app.app_context():
            db.drop_all()
            db.create_all()
    
    from peskos.login.routes import must_login
    from peskos.superadmin.routes import superadmin
    from peskos.admins.routes import admins
    from peskos.clients.routes import clients

    app.register_blueprint(superadmin)
    app.register_blueprint(admins)
    app.register_blueprint(clients)
    app.register_blueprint(must_login)

    return app

def role_required(fn):
    """
    learn more: https://flask.palletsprojects.com/en/2.2.x/patterns/viewdecorators/
    """
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        if current_user.roles[0].role == "superadmin":
            return fn(*args, **kwargs)
        elif current_user.roles[0].role == "admin":
            return fn(*args, **kwargs)
        else:
            flash("You need to be an admin to view this page.", "danger")
            return redirect(url_for("must_login.login"))
    return decorated_view

from peskos.models.admins import *
from peskos.models.client import *
from peskos.models.roles import *