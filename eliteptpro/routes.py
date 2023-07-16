from flask import render_template, redirect, request, flash, url_for, session, jsonify
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
        # with true attribute for "is_pt" and iterate over the list to add
        # any new trainers to trainers table
        trainers = list(User.query.filter(User.is_pt.is_(True)).all())
        for trainer in trainers:
            existing_trainer = Trainers.query.filter(
                Trainers.user_id == trainer.id).all()
            if not existing_trainer:
                new_trainer = Trainers(
                    user_id=trainer.id,
                    trainer_name=trainer.fname
                )
                db.session.add(new_trainer)
                db.session.commit()

        flash("Registration successful! Please Log in.")
        return redirect(url_for("home"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username is in db
        existing_user = User.query.filter(
            User.username == request.form.get("username").lower()).first()

        # check if password matches
        if existing_user:
            if check_password_hash(
                existing_user.password, request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                # check if user has true attribute for is_pt
                if existing_user.is_pt:
                    session["pt"] = True
                    flash("Welcome, {}".format(request.form.get("username")))
                    return redirect(url_for(
                    "pt_sessions", username=session["user"]))
                # if is_pt is false 
                else:
                    session.pop("pt", None)
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(url_for(
                    "my_sessions", username=session["user"]))
            
            # if password is incorrect
            else:
                flash("Username and/or Password incorrect!")
                return redirect(url_for("login"))

        # if username not in db
        else:
            flash("Username and/or Password incorrect!")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    # clear all session cookies
    session.clear()
    return redirect(url_for("home"))


@app.route("/my_sessions/<username>", methods=["GET", "POST"])
def my_sessions(username):
    # get user object that corresponds to the session user
    user = User.query.filter_by(username=session["user"]).first()
    sessions = Sessions.query.filter_by(user_id=user.id).all()
    return render_template("my_sessions.html", user=user, sessions=sessions)


@app.route("/pt_sessions/<username>",  methods=["GET", "POST"])
def pt_sessions(username):
    # get user object that corresponds to the session user
    user = User.query.filter_by(username=session["user"]).first()
    # get trainers object that corresponds to the current users id
    trainer = Trainers.query.filter_by(user_id=user.id).first()
    # get list of holidays that corresponds to the current trainers id
    holidays = Holidays.query.filter_by(trainer_id=trainer.id).all()
    # get all sessions in db that correspond to current trainers id
    sessions = Sessions.query.filter_by(trainer_id=trainer.id).all()
    return render_template("pt_sessions.html", user=user, trainer=trainer, holidays=holidays, sessions=sessions)


@app.route("/holiday", methods=["GET", "POST"])
def holiday():
    # get user object that corresponds to the session user
    user = User.query.filter_by(username=session["user"]).first()
    # get trainers object that corresponds to the current users id
    trainer = Trainers.query.filter_by(user_id=user.id).first()
    if request.method == "POST":
        # create ne instance of a holiday and add to db
        new_holiday = Holidays(
            trainer_id=trainer.id,
            date=request.form.get("date")
        )
        db.session.add(new_holiday)
        db.session.commit()
        flash("Holiday added successfully")
        return redirect(url_for("pt_sessions", username=session["user"]))
    return render_template("holiday.html")


@app.route("/book_session", methods=["GET", "POST"])
def book_session():
    # get user object that corresponds to the session user
    user = User.query.filter_by(username=session["user"]).first()
    # get trainers list that corresponds to the current users id
    trainers = list(Trainers.query.order_by(Trainers.trainer_name).all())
    # add new instance of session to db
    if request. method == "POST":
        trainer = request.form.get("trainer_name")
        selected_trainer = Trainers.query.filter_by(trainer_name=trainer).first()
        trainer_id = selected_trainer.id
        new_session = Sessions(
            user_id=user.id,
            trainer_id=trainer_id,
            name=request.form.get("name"),
            date=request.form.get("date"),
            time=request.form.get("time"),
            description=request.form.get("description")
        )
        db.session.add(new_session)
        db.session.commit()
        flash("Session booked successfully")
        return redirect(url_for("my_sessions", username=session["user"]))
    return render_template("book_session.html", user=user, trainers=trainers)


@app.route("/search_holidays", methods=["POST"])
def search_holidays():
    # get name of trainer from json sent and use that to return a list of dates 
    # booked as holidays by that trainer
    selected_trainer = request.json["selected_trainer"]
    selected_trainer_id = Trainers.query.filter_by(trainer_name=selected_trainer).first()
    trainer_id = selected_trainer_id.id
    holidays = Holidays.query.filter_by(trainer_id=trainer_id).all()
    holiday_dates = [holiday.date for holiday in holidays]
    return jsonify({'holidays': holiday_dates})


# @app.route("/search_times", methods=["POST"])
# def search_times():
#     selected_trainer = request.json["selected_trainer"]
#     selected_trainer_id = Trainers.query.filter_by(trainer_name=selected_trainer).first()
#     trainer_id = selected_trainer_id.id
#     selected_date = request.json["selected_date"]
#     sessions = Sessions.query.filter_by(trainer_id=trainer_id).all()
#     times = [session for session in sessions if session.date == selected_date]
#     return jsonify({'times': times})
