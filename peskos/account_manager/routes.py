from flask import Blueprint, flash, render_template, session, redirect, url_for
from flask_login import login_required, logout_user

from peskos import role_required

account_manager = Blueprint('account_manager', __name__)

@account_manager.route("/admin_dashboard")
@login_required
@role_required("account manager")
def dashboard():
    return render_template("account_manager/admin.html")

@account_manager.route("/admin_dashboard/clients")
@login_required
@role_required("account manager")
def clients():
    return render_template("account_manager/clients.html")

@account_manager.route("/admin_dashboard/reports")
@login_required
@role_required("account manager")
def reports():
    return render_template("account_manager/reports.html")

@account_manager.route("/logout")
def logout():
    logout_user()
    flash("Logout successful!", "info")
    return redirect(url_for("must_login.login"))
