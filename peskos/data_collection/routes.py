from flask import ( Blueprint, render_template )

data_collection = Blueprint('data_collection', __name__)

@data_collection.route("/data_collection")
def index():
    return render_template("data_collection/index.html")