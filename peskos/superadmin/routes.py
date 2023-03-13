import smtplib
from datetime import datetime, timedelta
from flask import Blueprint, flash, render_template, request, session, redirect, url_for
from flask_login import login_required, current_user, logout_user
from flask_mail import Message
from peskos.models.admins import Admins
from peskos.models.client import Clients
from peskos.models.roles import Role
from peskos.models.assign_traders import AssignTraders
from peskos.models.trading_records import TradingRecords
from peskos.models.verified_records import VerifiedRecords
from peskos.messages import LOGIN_DETAILS
from peskos._config import days_of_week
from peskos import db, role_required, config, bcrypt, mail
from peskos.superadmin.utils import checkrecords

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

def filter_assigned_clients() -> list:
    all_clients = Clients.query.all()
    filtered_clients = list()
    for client in all_clients:
        ta = AssignTraders.query.filter_by(assigned_client=client.id).first()
        if not ta:
            filtered_clients.append(client)
    return filtered_clients


@superadmin.route("/dashboard/admins", methods=["GET", "POST"])
@login_required
@role_required("super admin")
def admins():
    users = Admins.query.all()
    users.pop(0) # remove the super admin record

    clients = filter_assigned_clients()

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

        flash(f"User <strong>{fname} {lname}</strong> created Successfully!", 'success')
        return redirect(url_for("superadmin.admins"))

    return render_template("super_admin/admins.html", tab="admins", users=users, clients=clients, assigned=AssignTraders)

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

        flash(f"Admin <strong>{admin.first_name} {admin.last_name}</strong> edited successfully!", 'success')
        return redirect(url_for("superadmin.admins"))
        
    return render_template("super_admin/edit_admin.html", admin=admin)

@superadmin.route("/dashboard/admins/assign_client/<int:user_id>", methods=["POST"])
@login_required
@role_required("super admin")
def assign_client(user_id):
    assigned_client = Clients.query.get_or_404(int(request.form["assigned_client"]))
    trading_assistant = Admins.query.get_or_404(user_id)

    ats = AssignTraders(assigned_client=assigned_client.id, trading_assistant=trading_assistant.id)
    trading_assistant.is_assigned = True
    db.session.add(ats)
    db.session.add(trading_assistant)
    db.session.commit()
    flash(f"{trading_assistant.first_name} {trading_assistant.last_name} has been assigned client {assigned_client.name}!", "success")
    return redirect(url_for("superadmin.admins"))

@superadmin.route("/dashboard/admins/assign_client/modify_client/<int:user_id>", methods=["GET", "POST"])
@login_required
@role_required("super admin")
def modify_assigned_client(user_id):
    # This client variable contains also the trading assistant
    ta_and_client = AssignTraders.query.filter_by(trading_assistant=user_id).first()
    clients = filter_assigned_clients()

    if request.method == "POST":
        assigned_client = Clients.query.get_or_404(int(request.form["assigned_client"]))
        ta_and_client.assigned_client = assigned_client.id
        assigned_client.is_assigned = True
        db.session.add(ta_and_client)
        db.session.add(assigned_client)
        db.session.commit()
        flash(f"<strong>{ta_and_client.admin.first_name} {ta_and_client.admin.last_name}</strong> client has been changed to <strong>{assigned_client.name}!</strong>", "success")
        return redirect(url_for("superadmin.admins"))

    return render_template("super_admin/edit_assign.html", tab="Assign Client", data=ta_and_client, 
    clients=clients
    )

@superadmin.route("/dashboard/admins/unassign_ta/<int:user_id>")
@login_required
@role_required("super admin")
def unassign_ta(user_id):
    # delete the record containing him being assigned
    # get his admin record and set is_assigned to false
    trading_assistant = AssignTraders.query.filter_by(trading_assistant=user_id).first()
    admin_record = Admins.query.get_or_404(user_id)
    admin_record.is_assigned = False
    db.session.add(admin_record)
    db.session.delete(trading_assistant)
    db.session.commit()
    flash(f"<strong>{admin_record.first_name} {admin_record.last_name}</strong> has been unassigned!", "info")
    return redirect(url_for("superadmin.admins"))


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
    ta = TradingRecords.query.all()
    return render_template("super_admin/logs.html", tab="logs", ta=ta, clients=Clients)


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
        icd=icd, idcard_number=identity_card_no, account_number=account_no, 
        created_by=created_by, date_joined=datetime.utcnow().date())

        db.session.add(client)
        db.session.commit()

        flash(f"Client <strong>{full_name}</strong> created Successfully!", 'success')
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
    flash(f"Client {client.name} deleted!", "danger")
    return redirect(url_for("superadmin.clients"))

#######################################
#### REPORTS SECTION
####################################


@superadmin.route("/dashboard/reports")
@login_required
@role_required("super admin")
def reports():
    clients = Clients.query.all()
    return render_template("super_admin/reports.html", tab="All Reports", clients=clients)


@superadmin.route("/dashboard/reports/weekly")
@login_required
@role_required("super admin")
def weekly_reports():
    ready_clients_weekly = list()
    due = dict()
    clients = Clients.query.all()
    # rr = VerifiedRecords(is_initiated=True, has_payed=False, client_id=Clients.query.all()[1].id)
    # db.session.add(rr)
    # db.session.commit()
    for client in clients:
        record = checkrecords(client, "weekly")
        if record:
            ready_clients_weekly.append(client)
            due[client.id] = record
    return render_template("super_admin/weekly.html", tab="Weekly Trade-slips", clients=ready_clients_weekly, 
    due=due,timedelta=timedelta
    )


@superadmin.route("/dashboard/reports/monthly", methods=["GET","POST"])
@login_required
@role_required("super admin")
def check_monthly():
    ready_clients_weekly = list()
    clients = Clients.query.all()
    # rr = VerifiedRecords(is_initiated=True, has_payed=False, client_id=Clients.query.all()[1].id)
    # db.session.add(rr)
    # db.session.commit()
    for client in clients:
        record = checkrecords(client, "monthly")
        if record:
            ready_clients_weekly.append(client)
    return render_template("super_admin/monthly.html", tab="Monthly Reports", clients=ready_clients_weekly)


@superadmin.route("/dashboard/reports/yearly", methods=["GET","POST"])
@login_required
@role_required("super admin")
def check_yearly():
    ready_clients_weekly = list()
    clients = Clients.query.all()
    # rr = VerifiedRecords(is_initiated=True, has_payed=False, client_id=Clients.query.all()[1].id)
    # db.session.add(rr)
    # db.session.commit()
    for client in clients:
        record = checkrecords(client, "yearly")
        if record:
            ready_clients_weekly.append(client)
    return render_template("super_admin/yearly.html", tab="Yearly Reports", clients=ready_clients_weekly)

#######################################
#### SUMMARY SECTION
####################################

@superadmin.route("/dashboard/summary")
@login_required
@role_required("super admin")
def summary():
    return render_template("super_admin/summary.html", tab="summary")

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