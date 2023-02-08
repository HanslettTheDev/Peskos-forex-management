import json
from flask import Blueprint, flash, render_template, request, session, redirect, url_for
from flask_login import login_required, current_user, logout_user
import sqlalchemy

from peskos.models.admins import Admins
from peskos.models.roles import Role
from peskos import db, role_required, config, bcrypt

superadmin = Blueprint('superadmin', __name__)

@superadmin.route("/dashboard")
@superadmin.route("/dashboard/home")
@login_required
@role_required("super admin")
def dashboard():
    return render_template("super_admin/index.html", tab="home")


####################################
#### ADMINS SECTION
####################################
@superadmin.route("/dashboard/admins", methods=["GET", "POST"])
@login_required
@role_required("super admin")
def admins():
    users = Admins.query.all()
    users.pop(0)

    if request.method == "POST":
        
        fname = request.form["fname"]
        lname = request.form["lname"]
        user_role = request.form["user_role"].lower()
        email = request.form["mail"]
        hashed_password = bcrypt.generate_password_hash(config["default_passwords"][user_role])

        role = Role.query.filter_by(role=user_role).first()
        
        admin = Admins(first_name=fname, last_name=lname, password=hashed_password, email=email)

        admin.roles = role
        db.session.add(admin)
        db.session.commit()

        flash(f"User {fname} {lname} created Successfully!", 'success')
        return redirect(url_for("superadmin.admins"))

    return render_template("super_admin/admins.html", tab="admins", users=users)

@superadmin.route("/dashboard/admins/check_mail", methods=["POST"])
def check_mail():
    rdata = dict(message = "")
    data = request.get_json()
    admin = Admins.query.filter_by(email=data["mail"]).first()
    
    if not admin:
        return redirect(url_for("superadmin.admins")), 200
    
    rdata["message"] = "Email already taken"
    return rdata["message"], 404


@superadmin.route("/dashboard/admins/suspend/<int:user_id>")
@login_required
@role_required("super admin")
def suspend_admin(user_id):
    admin = Admins.query.get_or_404(user_id)
    # Change status to false
    if admin:
        admin.is_active = False
        db.session.add(admin)
        db.session.commit()
        flash(f"Admin {admin.first_name} is suspended", "info")
        return redirect(url_for("superadmin.admins"))
    return redirect(url_for("superadmin.admins"))

@superadmin.route("/dashboard/admins/activate/<int:user_id>")
@login_required
@role_required("super admin")
def activate_admin(user_id):
    admin = Admins.query.get_or_404(user_id)
    # Change status to false
    if admin:
        admin.is_active = True
        db.session.add(admin)
        db.session.commit()
        flash(f"Admin {admin.first_name} Activated", "info")
        return redirect(url_for("superadmin.admins"))
    return redirect(url_for("superadmin.admins"))

@superadmin.route("/dashboard/admins/edit/<int:user_id>", methods=["GET", "POST"])
@login_required
@role_required("super admin")
def edit_admin(user_id):
    admin = Admins.query.get_or_404(user_id)
    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        user_roles = request.form["user_role"].lower()
        email = request.form["mail"]

        role = Role.query.filter_by(role=user_roles).first()

        print(role)
        
        admin.first_name = fname
        admin.last_name = lname 
        admin.email = email
        admin.roles = role

        db.session.add(admin)
        db.session.commit()

        flash(f"Admin {fname} {lname} edited successfully!", 'success')
        return redirect(url_for("superadmin.admins"))
        
    return render_template("super_admin/edit_admin.html", admin=admin)


@superadmin.route("/dashboard/admins/delete/<int:user_id>")
@login_required
@role_required("super admin")
def delete_admin(user_id):
    admin = Admins.query.get_or_404(user_id)
    admin.roles = None
    db.session.delete(admin)
    db.session.commit()
    flash(f"Admin {admin.first_name} {admin.last_name} deleted!", "danger")
    return redirect(url_for("superadmin.admins"))


#######################################
#### LOGS SECTION
####################################


@superadmin.route("/dashboard/logs")
@login_required
@role_required("super admin")
def logs():
    return render_template("super_admin/logs.html", tab="logs")


#######################################
#### CLIENTS SECTION
####################################


@superadmin.route("/dashboard/clients")
@login_required
@role_required("super admin")
def clients():
    return render_template("super_admin/clients.html", tab="clients")


#######################################
#### REPORTS SECTION
####################################


@superadmin.route("/dashboard/reports")
@login_required
@role_required("super admin")
def reports():
    return render_template("super_admin/reports.html", tab="reports")


#######################################
#### SETTINGS SECTION
####################################


@superadmin.route("/dashboard/settings")
@login_required
@role_required("super admin")
def settings():
    return render_template("super_admin/settings.html", tab="settings")


#######################################
#### LOGOUT SECTION
####################################

@superadmin.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout successful!", "info")
    return redirect(url_for("must_login.login"))