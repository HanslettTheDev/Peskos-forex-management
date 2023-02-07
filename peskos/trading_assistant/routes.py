from flask import ( Blueprint, render_template, request )
from flask_login import login_required
from peskos import role_required

trading_assistant = Blueprint('trading_assistant', __name__)

@trading_assistant.route("/trading_assistant", methods=["POST", "GET"])
@login_required
@role_required("trading assistant")
def index():
    return render_template("trading_assistant/index.html")

@trading_assistant.route("/trading_assistant/checkname", methods=["POST"])
@login_required
@role_required("trading assistant")
def check_name():
    rdata = dict(message = "", type="")
    data = request.get_json()
    
    #check if user has already filled for the current day
    if data["name"] != "to implment":
        rdata["message"] = "User has already filled for today"
        rdata["type"] = "is-danger"
        return rdata, 404

    #if it reached here, then can fill
    rdata["message"] = "User can fill"
    rdata["error"] = "is-success"
    return rdata