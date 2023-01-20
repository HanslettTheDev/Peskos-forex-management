from flask import (Blueprint, render_template, request, session, redirect, 
url_for, flash
)
from flask_login import login_user
from peskos import login_manager, bcrypt
from peskos.models.admins import Admins
# from flask_login import login_required, current_user

must_login = Blueprint('must_login', __name__)

@must_login.route("/", methods=["GET", "POST"])
@must_login.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "" or password == "":
            flash("Fields can't be empty", "danger")
            return render_template("login.html")
        try:
            admin = Admins.query.filter_by(login_id=int(username)).first()
        except ValueError:
            admin = Admins.query.filter_by(username=username).first() if username.startswith("@") else None
        
        if not admin:
            flash("Password or email incorrect", "danger")
            return render_template("login.html")

        if bcrypt.check_password_hash(admin.password, password) == False:
            flash("Password or email incorrect", "danger")
            return render_template("login.html")

        login_user(admin)
        flash("Login Successful!", "success")
        return redirect(url_for("superadmin.dashboard"))
    else:
        return render_template("login.html")