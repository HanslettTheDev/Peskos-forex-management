from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_user
from peskos import bcrypt, _ROUTE_CONFIG
from peskos.models.admins import Admins

must_login = Blueprint("must_login", __name__)


@must_login.route("/", methods=["GET", "POST"])
@must_login.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for(_ROUTE_CONFIG["roles_path"][current_user.roles.role]))

    if request.method == "POST":
        email = request.form["mail"].strip()
        password = request.form["password"].strip()

        admin = Admins.query.filter_by(email=email).first()

        if not admin:
            flash("Password or email incorrect", "danger")
            return render_template("login/login.html")

        if bcrypt.check_password_hash(admin.password, password) == False:
            flash("Password or email incorrect", "danger")
            return render_template("login/login.html")

        login_user(admin)
        next_page = request.args.get("next")
        return (
            redirect(next_page)
            if next_page
            else redirect(url_for(_ROUTE_CONFIG["roles_path"][admin.roles.role]))
        )

    else:
        return render_template("login/login.html")
