from flask import ( Blueprint, render_template, request )
from flask_login import login_required
from peskos import role_required

ta_analyst = Blueprint('ta_analyst', __name__)

@ta_analyst.route("/ta_dashboard", methods=["POST", "GET"])
@login_required
@role_required("technical analyst")
def dashboard():
    return render_template("ta_analyst/index.html")