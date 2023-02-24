from flask import Blueprint, flash, render_template, request, session, redirect, url_for
from flask_login import current_user, login_required, logout_user

from peskos import role_required, db
from peskos.models.client import Clients

account_manager = Blueprint('account_manager', __name__)

@account_manager.route("/account_manager")
@login_required
@role_required("account manager")
def dashboard():
    return render_template("account_manager/index.html", tab="Home")

@account_manager.route("/account_manager/clients", methods=["GET", "POST"])
@login_required
@role_required("account manager")
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
        return redirect(url_for("account_manager.clients"))
    return render_template("account_manager/clients.html", tab="clients", clients=clients)

@account_manager.route("/account_manager/clients/edit/<int:client_id>", methods=["GET", "POST"])
@login_required
@role_required("account manager")
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
        return redirect(url_for("account_manager.clients"))

    return render_template("account_manager/edit_client.html", tab="clients", client=client)

@account_manager.route("/account_manager/clients/delete/<int:client_id>")
@login_required
@role_required("account manager")
def delete_client(client_id):
    client = Clients.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    flash(f"Client {client.name} deleted!", "danger")
    return redirect(url_for("account_manager.clients"))


@account_manager.route("/account_manager/reports")
@login_required
@role_required("account manager")
def reports():
    return render_template("account_manager/reports.html", tab="reports")

@account_manager.route("/logout")
def logout():
    logout_user()
    flash("Logout successful!", "info")
    return redirect(url_for("must_login.login"))
