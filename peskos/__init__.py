from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from peskos.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "routes.login"
login_manager.login_message_category = "info"

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    # login_manager.init_app(app)
    bcrypt.init_app(app)

    from peskos.superadmin.routes import superadmin
    from peskos.admins.routes import admins
    from peskos.clients.routes import clients

    app.register_blueprint(superadmin)
    app.register_blueprint(admins)
    app.register_blueprint(clients)

    return app