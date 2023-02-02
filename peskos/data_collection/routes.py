from flask import ( Blueprint, render_template, request )

data_collection = Blueprint('data_collection', __name__)

@data_collection.route("/data_collection")
def index():
    return render_template("data_collection/index.html")

@data_collection.route("/data_collection/checkname", methods=["POST"])
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