from flask import (Blueprint, render_template, request, session, redirect, 
url_for, flash
)
from flask_login import login_user
from flask_login import current_user
from peskos import bcrypt, config
from peskos.models.admins import Admins

must_login = Blueprint('must_login', __name__)

@must_login.route("/", methods=["GET", "POST"])
@must_login.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for(config["roles_path"][current_user.roles.role]))

    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        try:
            admin = Admins.query.filter_by(login_id=int(username)).first()
        except ValueError:
            admin = Admins.query.filter_by(username=username).first() if username.startswith("@") else None

        if not admin:
            flash("Password or email incorrect", "danger")
            return render_template("login/login.html")
        try:    
            if bcrypt.check_password_hash(admin.password, password) == False:
                flash("Password or email incorrect", "danger")
                return render_template("login.html")
        except ValueError:
            if admin.password != password:
                flash("Password or email incorrect", "danger")
                return render_template("login/login.html")

        login_user(admin)
        return redirect(url_for(config["roles_path"][current_user.roles.role]))
        
    else:
        return render_template("login/login.html")