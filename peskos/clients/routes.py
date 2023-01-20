from flask import Blueprint, render_template, redirect, url_for
# from flask_login import login_required, current_user

clients = Blueprint('clients', __name__)

# @clients.route("/login", methods=["GET", "POST"])
# def login():
#     if current_user.is_authenticated():
#         return redirect(url_for("home"))
#     return render_template("login.html")

# @clients.route("/dashboard")
# @login_required
# def home():
#     return render_template("layout.html")
