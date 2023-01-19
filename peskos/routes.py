from flask import render_template

from peskos import app

@app.route("/home")
def home():
    return render_template("index.html")