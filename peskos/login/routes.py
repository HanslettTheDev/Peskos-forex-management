from flask import Blueprint, render_template, redirect, url_for
from peskos import login_manager
# from flask_login import login_required, current_user

must_login = Blueprint('must_login', __name__)

@must_login.route("/", methods=["GET", "POST"])
@must_login.route("/login", methods=["GET", "POST"])
def login():
    # if current_user.is_authenticated():
    #     return redirect(url_for("home"))
    return render_template("login.html")