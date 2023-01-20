from flask import Flask, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
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

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    seeder.init_app(app, db)
    
    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()
    
    from peskos.login.routes import must_login
    from peskos.superadmin.routes import superadmin
    from peskos.admins.routes import admins
    from peskos.clients.routes import clients

    app.register_blueprint(superadmin)
    app.register_blueprint(admins)
    app.register_blueprint(clients)
    app.register_blueprint(must_login)

    return app

def role_required(role="superadmin"):
    """
    learn more: https://flask.palletsprojects.com/en/2.2.x/patterns/viewdecorators/
    """
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if session.get("role") == None or role == "superadmin":
                return redirect(url_for("superadmin.superadmin_dashboard"))
            if session.get("role") == "admin" and role == "admin":
                return redirect(url_for("admins.admindashboard"))
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

from peskos.models.admin_models import *
from peskos.models.client_models import *
from peskos.models.role_models import *
