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

        # create new instance of a user
        new_user = User(
            username=request.form.get("username").lower(),
            fname=request.form.get("fname").lower(),
            lname=request.form.get("lname").lower(),
            password=generate_password_hash(request.form.get("password")),
            is_pt=bool(True if request.form.get("is_pt") else False)
        )

        db.session.add(new_user)
        db.session.commit()

        # once new user is commited to db retrieve a list of all users
        # with true attribute for "is_pt"and iterate over the list to add
        # any new trainers to trainers table
        trainers = list(User.query.filter(User.is_pt.is_(True)).all())
        for trainer in trainers:
            new_trainer = Trainers(
                user_id=trainer.id,
                trainer_name=trainer.fname
            )
            db.session.add(new_trainer)
            db.session.commit()

        session["user"] = request.form.get("username").lower()
        flash("Registration successful!")
        return redirect(url_for(
            "my_sessions", username=session["user"]))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        existing_user = User.query.filter(
            User.username == request.form.get("username").lower()).first()

        if existing_user:
            if check_password_hash(
                existing_user.password, request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                if existing_user.is_pt:
                    session["pt"] = True
                else:
                    session.pop("pt", None)
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(url_for(
                    "my_sessions", username=session["user"]))
            
            else:
                flash("Username and/or Password incorrect!")
                return redirect(url_for("login"))

        else:
            flash("Username and/or Password incorrect!")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/my_sessions/<username>", methods=["GET", "POST"])
def my_sessions(username):
    # get user object that corresponds to the session user
    user = User.query.filter_by(username=session["user"]).first()
    return render_template("my_sessions.html", user=user)


@app.route("/book_session", methods=["GET", "POST"])
def book_session():
    return render_template("book_session.html")