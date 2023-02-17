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
        email = request.form["mail"].strip()
        password = request.form["password"].strip()

        admin = Admins.query.filter_by(email=email).first()

        if not admin:
            flash("Password or email incorrect", "danger")
            return render_template("login/login.html")
    
        if bcrypt.check_password_hash(admin.password, password) == False:
            flash("Password or email incorrect", "danger")
            return render_template("login.html")

        login_user(admin)
        return redirect(url_for(config["roles_path"][admin.roles.role]))
        
    else:
        return render_template("login/login.html")