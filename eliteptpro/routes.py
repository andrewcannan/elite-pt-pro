from flask import render_template, redirect, request, flash, url_for
from eliteptpro import app, db
from eliteptpro.models import User, Trainers, Holidays, Sessions
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/")
def home():
    return render_template("homepage.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")
