from flask import render_template
from eliteptpro import app, db


@app.route("/")
def home():
    return render_template("homepage.html")
