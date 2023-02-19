import json
import smtplib
from traceback import format_exc
from flask import Blueprint, flash, render_template, request, session, redirect, url_for
from flask_login import login_required, current_user, logout_user
from flask_mail import Message

from peskos.models.admins import Admins
from peskos.models.client import Clients
from peskos.models.roles import Role
from peskos.messages import LOGIN_DETAILS
from peskos import db, role_required, config, bcrypt, mail

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

    # delete modal settings
    # modal_settings = {
    #     "message": "Are you sure you want to delete this admin?",
    #     "route_name": "superadmin.delete_admin",
    #     "has_variable": True,
    # }

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
        

        user_role = request.form["user_role"].lower()
        role = Role.query.filter_by(role=user_role).first()

        admin.first_name = request.form["fname"]
        admin.last_name = request.form["lname"] 
        admin.email = request.form["mail"]
        admin.roles = role

        # check the passwords to see if it's the same default password 
        # so as not overwrite the passwords
        def check_password():
            for key, value in config["default_passwords"].items():
                if bcrypt.check_password_hash(admin.password, value):
                    if key != user_role:
                        return bcrypt.generate_password_hash(config["default_passwords"][user_role])
                    return bcrypt.generate_password_hash(config["default_passwords"][key])
                    
            return admin.password
        
        admin.password = check_password()

        db.session.add(admin)
        db.session.commit()

        flash(f"Admin {admin.first_name} {admin.last_name} edited successfully!", 'success')
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


@superadmin.route("/dashboard/admins/send_mail/<int:user_id>")
@login_required
@role_required("super admin")
def send_mail(user_id):
    user = Admins.query.get_or_404(user_id)
    msg = Message("Peskos Login Information", recipients=[user.email])
    msg.html = LOGIN_DETAILS.format(name=user.first_name, role=user.roles.role, email=user.email, password=config["default_passwords"][user.roles.role])
    try:
        mail.send(msg)
    except smtplib.SMTPRecipientsRefused:
        flash("Email does not exist or it's incorrect", "danger")
        return redirect(url_for("superadmin.admins"))
    except smtplib.smtpauthenticationerror:
        flash("Unexpected server error, please try again later!", "danger")
        return redirect(url_for("superadmin.admins"))
    
    # No errors occured
    flash("Email sent successfully to {0}".format(user.email), "success")
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


@superadmin.route("/dashboard/clients", methods=["GET", "POST"])
@login_required
@role_required("super admin")
def clients():
    clients = Clients.query.all()

    if request.method == "POST":
        full_name = request.form["full-name"]
        email = request.form["mail"]
        broker = request.form["broker"]
        account_type = request.form["account-type"]
        phone_no = request.form["phone-no"]
        phone_no_2 = request.form["phone-no-2"]
        icd = request.form["icd"]
        identity_card_no = request.form["idno"]
        created_by = current_user.id
        account_no = request.form["acn"]
        
        client = Clients(name=full_name, email=email, broker=broker, 
        account_type=account_type, phone_number=phone_no, second_number=phone_no_2,
        icd=icd, idcard_number=identity_card_no, account_number=account_no, created_by=created_by)

        db.session.add(client)
        db.session.commit()

        flash(f"Client {full_name} created Successfully!", 'success')
        # save clients to the database and work on the trading assistant section and logs
        return redirect(url_for("superadmin.clients"))

    return render_template("super_admin/clients.html", tab="clients", clients=clients)


@superadmin.route("/dashboard/clients/edit/<int:client_id>", methods=["GET", "POST"])
@login_required
@role_required("super admin")
def edit_client(client_id):
    client = Clients.query.get_or_404(client_id)

    if request.method == "POST":
        client.name = request.form["full-name"]
        client.email = request.form["mail"]
        client.broker = request.form["broker"]
        client.account_type = request.form["account-type"]
        client.phone_number = request.form["phone-no"]
        client.second_number = request.form["phone-no-2"]
        client.icd = request.form["icd"]
        client.idcard_number = request.form["idno"]
        client.account_number = request.form["acn"]
        client.created_by = current_user.id
        
        db.session.add(client)
        db.session.commit()

        flash(f"Client {client.name} edited successfully!", 'info')
        return redirect(url_for("superadmin.clients"))

    return render_template("super_admin/edit_client.html", tab="clients", client=client)

@superadmin.route("/dashboard/clients/delete/<int:client_id>")
@login_required
@role_required("super admin")
def delete_client(client_id):
    client = Clients.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    flash(f"Admin {client.name} deleted!", "danger")
    return redirect(url_for("superadmin.clients"))

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