from flask import Blueprint, flash, render_template, session, redirect, url_for
from flask_login import login_required, logout_user

from peskos import role_required

admins = Blueprint('admins', __name__)

@admins.route("/admin_dashboard")
@login_required
@role_required("admin")
def dashboard():
    return render_template("admins/admin.html")

@admins.route("/admin_dashboard/clients")
@login_required
@role_required("admin")
def clients():
    return render_template("admins/clients.html")

@admins.route("/admin_dashboard/reports")
@login_required
@role_required("admin")
def reports():
    return render_template("admins/reports.html")

@admins.route("/logout")
def logout():
    logout_user()
    flash("Logout successful!", "info")
    return redirect(url_for("must_login.login"))
