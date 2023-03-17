from datetime import datetime as d
from datetime import timedelta

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, logout_user

from peskos import db, role_required
from peskos.models.assign_traders import AssignTraders
from peskos.models.trading_records import TradingRecords

trading_assistant = Blueprint("trading_assistant", __name__)


@trading_assistant.route("/trading_assistant", methods=["POST", "GET"])
@login_required
@role_required("trading assistant")
def index():
    ta = TradingRecords.query.filter_by(
        name=f"{current_user.first_name} {current_user.last_name}"
    ).all()

    assigned = AssignTraders.query.filter_by(trading_assistant=current_user.id).first()

    current_time = d.now().date()
    try:
        last_recorded_time = ta[-1].date_entered
    except IndexError:
        last_recorded_time = None
    can_fill_form = True
    next_day = None

    if last_recorded_time and not last_recorded_time < current_time:
        can_fill_form = False
        next_day = d.now() + timedelta(days=1)

    if request.method == "POST":
        full_name = request.form["name"]
        account_number = request.form["account_number"]
        initial_amount = request.form["initial_amount"]
        final_amount = request.form["final_amount"]
        profit = request.form["profit"]
        statement = request.form["statement"]

        trading_record = TradingRecords(
            name=full_name,
            account_number=account_number,
            initial_amount=initial_amount,
            final_amount=final_amount,
            profit=profit,
            acc_statement=statement,
            date_entered=d.utcnow().date(),
        )

        db.session.add(trading_record)
        db.session.commit()

        flash(
            f"Trading Record with account number #{account_number} added Successfully!",
            "success",
        )
        return redirect(url_for("trading_assistant.show_info"))
    return render_template(
        "trading_assistant/index.html",
        can_fill_form=can_fill_form,
        next_day=next_day,
        assigned=assigned,
    )


@trading_assistant.route("/trading_assistant/info")
@login_required
@role_required("trading assistant")
def show_info():
    return render_template("/trading_assistant/info.html")


#######################################
#### LOGOUT SECTION
####################################


@trading_assistant.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout successful!", "info")
    return redirect(url_for("must_login.login"))


# @trading_assistant.route("/trading_assistant/checkname", methods=["POST"])
# @login_required
# @role_required("trading assistant")
# def check_name():
#     rdata = dict(message = "", type="")
#     data = request.get_json()

#     #check if user has already filled for the current day
#     if data["name"] != "to implment":
#         rdata["message"] = "User has already filled for today"
#         rdata["type"] = "is-danger"
#         return rdata, 404

#     #if it reached here, then can fill
#     rdata["message"] = "User can fill"
#     rdata["error"] = "is-success"
#     return rdata
