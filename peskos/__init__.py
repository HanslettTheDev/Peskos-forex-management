import json
import os
from functools import lru_cache, wraps

from flask import Flask, flash, redirect, request, url_for
from flask_login import current_user, logout_user

from peskos.config import Config
from peskos.extensions import bcrypt, db, login_manager, mail, migrate

path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "db.sqlite")

config_path = os.path.join(os.getcwd(), "config.json")


# FIXME: this utils should be inside a config python file and imported here
@lru_cache(maxsize=1)
def get_config():
    with open(config_path, "r", encoding="utf8") as config:
        data = json.load(config)
    return data


_CONFIG = get_config()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    # FIXME: those imports inside a method are scary... is there a specific
    # reason for doing that ?
    # usually we can tolarate inside import to prevent "circular import" of a
    # module, i don't know if it's the case here ?
    from peskos.account_manager.routes import account_manager
    from peskos.login.routes import must_login
    from peskos.superadmin.routes import superadmin
    from peskos.ta_analyst.routes import ta_analyst
    from peskos.trading_assistant.routes import trading_assistant

    app.register_blueprint(must_login)
    app.register_blueprint(superadmin)
    app.register_blueprint(account_manager)
    app.register_blueprint(ta_analyst)
    app.register_blueprint(trading_assistant)

    return app


def role_required(role: str):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if current_user.roles.role == role and request.path.startswith(
                _CONFIG["roles"][role]
            ):
                # check the accounts state first
                if not current_user.is_active:
                    logout_user()
                    flash("Access denied! Your Account has been suspended", "danger")
                    return redirect(url_for("must_login.login"))
                # check if the requested route is their default homepages and return that route
                return fn(*args, **kwargs)
            else:
                logout_user()
                flash(
                    "Access denied! you're not allowed to view this route. Login to proceed",
                    "danger",
                )
                return redirect(url_for("must_login.login", next=request.url))

        return decorated_view

    return wrapper
