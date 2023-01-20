from flask import Blueprint, render_template, session, redirect, url_for
from flask_login import login_required, current_user
from peskos import role_required

superadmin = Blueprint('superadmin', __name__)

@superadmin.route("/dashboard")
@login_required
# @role_required()
def dashboard():
    print(session)
    return render_template("index.html")
