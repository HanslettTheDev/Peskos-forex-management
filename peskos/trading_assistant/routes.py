from flask import ( Blueprint, flash, redirect, render_template, request, url_for )
from flask_login import current_user, login_required
from peskos import role_required, db
from peskos.models.trading_records import TradingRecords

trading_assistant = Blueprint('trading_assistant', __name__)

@trading_assistant.route("/trading_assistant", methods=["POST", "GET"])
@login_required
@role_required("trading assistant")
def index():
    ta = TradingRecords.query.filter_by(name=f"{current_user.first_name} {current_user.last_name}").all()
    print(ta)
    if request.method == "POST":
        full_name = request.form["name"]
        account_number = request.form["account_number"]
        initial_amount = request.form["initial_amount"]
        final_amount = request.form["final_amount"]
        profit = request.form["profit"]
        statement = request.form["statement"]
        
        trading_record = TradingRecords(name=full_name, account_number=account_number, initial_amount=initial_amount,
        final_amount=final_amount, profit=profit, acc_statement=statement)

        db.session.add(trading_record)
        db.session.commit()

        flash(f"Trading Record with account number #{account_number} added Successfully!", 'success')
        return redirect(url_for("trading_assistant.show_info"))
    return render_template("trading_assistant/index.html")

@trading_assistant.route("/trading_assistant/info")
@login_required
@role_required("trading assistant")
def show_info():
    return render_template("/trading_assistant/info.html")

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