from flask import Blueprint, render_template, session, redirect, url_for
from flask_login import login_required, current_user
from peskos import role_required

admins = Blueprint('admins', __name__)

@admins.route("/admin_dashboard")
@login_required
def dashboard():
    print(session.get("role"))
    return render_template("admin.html")
