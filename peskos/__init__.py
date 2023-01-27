from functools import wraps
import os
from flask import Flask, flash, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, logout_user
from flask_bcrypt import Bcrypt
from flask_seeder import FlaskSeeder
from peskos.config import Config

db = SQLAlchemy(session_options={"autoflush": False})
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
    
    from peskos.login.routes import must_login
    from peskos.superadmin.routes import superadmin
    from peskos.admins.routes import admins

    app.register_blueprint(superadmin)
    app.register_blueprint(admins)
    app.register_blueprint(must_login)

    return app

def role_required(role:str, state:bool=True):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if current_user.roles.role == 'admin' and role == "admin":
                if current_user.is_active and state:
                    return fn(*args, **kwargs)
                else:
                    logout_user()
                    flash("Access denied! Your Account has been suspended", "danger")
                    return redirect(url_for('must_login.login'))

            if current_user.roles.role == 'superadmin' and role == "superadmin":
                if current_user.is_active and state:
                    return fn(*args, **kwargs)
                else:
                    logout_user()
                    flash("Access denied! Your Account has been suspended", "danger")
                    return redirect(url_for('must_login.login'))
            else:
                logout_user()
                flash("Access denied! Log in to a superadmin/admin account to proceed", "danger")
                return redirect(url_for('must_login.login', next=request.url))
        return decorated_view
    return wrapper