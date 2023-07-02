from flask import render_template, redirect, request, flash, url_for, session
from eliteptpro import app, db
from eliteptpro.models import User, Trainers, Holidays, Sessions
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/")
def home():
    return render_template("homepage.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists
        existing_user = User.query.filter(
            User.username == request.form.get("username").lower()).all()

        if existing_user:
            flash("Username already eists")
            return redirect(url_for("register"))

        new_user = User(
            username=request.form.get("username").lower(),
            password=generate_password_hash(request.form.get("password")),
            is_pt=bool(True if request.form.get("is_pt") else False)
        )
        db.session.add(new_user)
        db.session.commit()

        session["user"] = request.form.get("username").lower()
        flash("Registration successful!")
    return render_template("register.html")
