from flask import render_template, redirect, request, flash, url_for,\
    session, jsonify
from eliteptpro import app, db
from eliteptpro.models import User, Trainers, Holidays, PTsessions
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/")
def home():
    return render_template("homepage.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Adds new instance of user to database if not already existing.
    Checks if new user is a trainer and adds to trainers table.
    """
    if request.method == "POST":
        # check if username already exists
        existing_user = User.query.filter(
            User.username == request.form.get("username").lower()).all()

        if existing_user:
            flash("Username already exists")
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
    """
    Handles login of user and redirects based on session cookies
    """
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
                # redirect admin to manage page
                if session["user"] == "admin":
                    return redirect(url_for("manage"))
                # redirect normal user to sessions
                else:
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
    """
    Queries database to populate and display members page
    - params:
        string: username
    """
    # get user object that corresponds to the session user
    user = User.query.filter_by(username=session["user"]).first()
    pt_sessions = PTsessions.query.filter_by(user_id=user.id).all()
    for pt_session in pt_sessions:
        trainer_id = pt_session.trainer_id
        selected_trainer = Trainers.query.filter_by(id=trainer_id).first()
        trainer_name = selected_trainer.trainer_name
        pt_session.trainer_name = trainer_name
    return render_template(
        "my_sessions.html", user=user, pt_sessions=pt_sessions)


@app.route("/pt_sessions/<username>",  methods=["GET", "POST"])
def pt_sessions(username):
    """
    Queries database to populate and display trainers page
    - params:
        string: username
    """
    # get user object that corresponds to the session user
    user = User.query.filter_by(username=session["user"]).first()
    # get trainers object that corresponds to the current users id
    trainer = Trainers.query.filter_by(user_id=user.id).first()
    # get list of holidays that corresponds to the current trainers id
    holidays = Holidays.query.filter_by(trainer_id=trainer.id).all()
    # get all sessions in db that correspond to current trainers id
    pt_sessions = PTsessions.query.filter_by(trainer_id=trainer.id).all()
    return render_template("pt_sessions.html", user=user,
                           trainer=trainer, holidays=holidays,
                           pt_sessions=pt_sessions)


@app.route("/holiday", methods=["GET", "POST"])
def holiday():
    """
    Add new instance of holiday to database
    """
    # get user object that corresponds to the session user
    user = User.query.filter_by(username=session["user"]).first()
    # get trainers object that corresponds to the current users id
    trainer = Trainers.query.filter_by(user_id=user.id).first()
    if request.method == "POST":
        # create new instance of a holiday and add to db
        new_holiday = Holidays(
            trainer_id=trainer.id,
            date=request.form.get("date")
        )
        db.session.add(new_holiday)
        db.session.commit()
        flash("Holiday added successfully")
        return redirect(url_for("pt_sessions", username=session["user"]))
    return render_template("holiday.html")


@app.route("/delete_holiday/<int:holiday_id>")
def delete_holiday(holiday_id):
    """
    Deletes instance of holiday from database
    - params:
        int: holiday_id
    """
    # get user object that corresponds to the session user
    user = User.query.filter_by(username=session["user"]).first()
    if user.is_pt != True and (
            session["user"] != "admin"):
        flash("you do not have permission to delete this training session")
        return redirect(url_for("home"))

    # deletes holiday from the holidays table in db
    holiday = Holidays.query.get_or_404(holiday_id)
    db.session.delete(holiday)
    db.session.commit()
    if session["user"] == "admin":
        return redirect(url_for("manage"))
    return redirect(url_for("pt_sessions", username=session["user"]))


@app.route("/book_pt_session", methods=["GET", "POST"])
def book_pt_session():
    """
    Add instance of pt session to database
    """
    # get user object that corresponds to the session user
    user = User.query.filter_by(username=session["user"]).first()
    # get trainers list that corresponds to the current users id
    trainers = list(Trainers.query.order_by(Trainers.trainer_name).all())
    # add new instance of session to db
    if request.method == "POST":
        trainer = request.form.get("trainer_name")
        selected_trainer = Trainers.query.filter_by(
            trainer_name=trainer).first()
        trainer_id = selected_trainer.id
        new_pt_session = PTsessions(
            user_id=user.id,
            trainer_id=trainer_id,
            name=request.form.get("name"),
            date=request.form.get("date"),
            time=request.form.get("time"),
            description=request.form.get("description")
        )
        db.session.add(new_pt_session)
        db.session.commit()
        flash("Session booked successfully")
        return redirect(url_for("my_sessions", username=session["user"]))
    return render_template(
        "book_pt_session.html", user=user, trainers=trainers)


@app.route("/edit_pt_session/<int:pt_session_id>", methods=["GET", "POST"])
def edit_pt_session(pt_session_id):
    """
    Edit instance of pt session in database
    - params:
        int: pt_session_id
    """
    # get user object that corresponds to the session user
    user = User.query.filter_by(username=session["user"]).first()
    # get trainers list that corresponds to the current users id
    trainers = list(Trainers.query.order_by(Trainers.trainer_name).all())
    # retrieve pt session from db or throw 404 if non existent
    pt_session = PTsessions.query.get_or_404(pt_session_id)
    # add trainers name to pt_session for displaying
    trainer_id = pt_session.trainer_id
    selected_trainer = Trainers.query.filter_by(id=trainer_id).first()
    trainer_name = selected_trainer.trainer_name
    pt_session.trainer_name = trainer_name
    if user.id != pt_session.user_id and (
            session["user"] != "admin") and (user.is_pt != True):
        flash("you do not have permission to edit this training session")
        return redirect(url_for("home"))

    if request.method == "POST":
        # gets trainers id by query with the name selected in the form
        trainer = request.form.get("trainer_name")
        selected_trainer = Trainers.query.filter_by(
            trainer_name=trainer).first()
        trainer_id = selected_trainer.id
        # edit row in table
        pt_session.trainer_id = trainer_id,
        pt_session.name = request.form.get("name"),
        pt_session.date = request.form.get("date"),
        pt_session.time = request.form.get("time"),
        pt_session.description = request.form.get("description")
        db.session.commit()

        if user.is_pt:
            return redirect(url_for("pt_sessions", username=session["user"]))
        elif session["user"] == "admin":
            return redirect(url_for("manage", username=session["user"]))
        else:
            return redirect(url_for("my_sessions", username=session["user"]))
    return render_template("edit_pt_session.html", user=user,
                           trainers=trainers, pt_session=pt_session)


@app.route("/delete_pt_session/<int:pt_session_id>")
def delete_pt_session(pt_session_id):
    # get user object that corresponds to the session user
    user = User.query.filter_by(username=session["user"]).first()
    # deletes pt session from the sessions table in db
    pt_session = PTsessions.query.get_or_404(pt_session_id)
    if user.id != pt_session.user_id and (
            session["user"] != "admin") and (user.is_pt != True):
        flash("you do not have permission to delete this training session")
        return redirect(url_for("home"))

    db.session.delete(pt_session)
    db.session.commit()
    if user.is_pt:
        return redirect(url_for("pt_sessions", username=session["user"]))
    elif session["user"] == "admin":
        return redirect(url_for("manage"))
    else:
        return redirect(url_for("my_sessions", username=session["user"]))


@app.route("/search_holidays", methods=["POST"])
def search_holidays():
    """
    Get name of trainer from json sent and use that to return a list of dates
    booked as holidays by that trainer
    """
    selected_trainer = request.json["selected_trainer"]
    selected_trainer_id = Trainers.query.filter_by(
        trainer_name=selected_trainer).first()
    trainer_id = selected_trainer_id.id
    holidays = Holidays.query.filter_by(trainer_id=trainer_id).all()
    holiday_dates = [holiday.date for holiday in holidays]
    return jsonify({'holidays': holiday_dates})


@app.route("/search_times", methods=["POST"])
def search_times():
    """
    Get name of trainer and date from json, retrieve trainer id using name
    and query sessions table to retrieve list of times for selected trainer
    for that specific date
    """
    selected_trainer = request.json["selected_trainer"]
    selected_trainer_id = Trainers.query.filter_by(
        trainer_name=selected_trainer).first()
    trainer_id = selected_trainer_id.id
    selected_date = request.json["selected_date"]
    pt_sessions = PTsessions.query.filter_by(
        trainer_id=trainer_id, date=selected_date).all()
    times = [pt_session.time for pt_session in pt_sessions]
    times_string = [time.strftime('%H:%M') for time in times]
    return jsonify({'times': times_string})


@app.route("/manage", methods=["GET"])
def manage():
    """
    Queries database to return data to populate and display manage page
    """
    if "user" not in session or session["user"] != "admin":
        flash("You do not have permission to view admin page")
        return redirect(url_for("home"))
    # retrieve list of all users in db excluding admin
    users = User.query.filter(User.username != "admin").order_by(
        User.username).all()
    # retrieve list of all trainers in db
    trainers = Trainers.query.order_by(Trainers.trainer_name).all()
    # retrieve list of all pt sessions in db
    pt_sessions = PTsessions.query.order_by(PTsessions.date).all()
    for pt_session in pt_sessions:
        trainer_id = pt_session.trainer_id
        selected_trainer = Trainers.query.filter_by(id=trainer_id).first()
        trainer_name = selected_trainer.trainer_name
        pt_session.trainer_name = trainer_name
    # retrieve list of all holidays in db
    holidays = Holidays.query.order_by(Holidays.date).all()
    for holiday in holidays:
        trainer_id = holiday.trainer_id
        selected_trainer = Trainers.query.filter_by(id=trainer_id).first()
        trainer_name = selected_trainer.trainer_name
        holiday.trainer_name = trainer_name
    return render_template("manage.html", users=users,
                           pt_sessions=pt_sessions,
                           holidays=holidays, trainers=trainers)


@app.route("/edit_user/<int:user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    """
    Edits instance of user in database
    - params:
        int: user_id
    """
    # get user object that corresponds to the user id
    user = User.query.filter_by(id=user_id).first()
    if "user" not in session or session["user"] != "admin":
        flash("You do not have permission to edit user")
        return redirect(url_for("home"))

    if request.method == "POST":
        user.username = request.form.get("username")
        user.fname = request.form.get("fname")
        user.lname = request.form.get("lname")
        user.password = user.password
        user.is_pt = bool(True if request.form.get("is_pt") else False)
        db.session.commit()
        return redirect(url_for("manage"))

    return render_template("edit_user.html", user=user)


@app.route("/delete_user/<int:user_id>")
def delete_user(user_id):
    """
    Deletes user from database
    - params:
        int: user_id
    """
    if "user" not in session or session["user"] != "admin":
        flash("You do not have permission to delete user")
        return redirect(url_for("home"))
    else:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("manage"))


@app.route("/delete_trainer/<int:trainer_id>")
def delete_trainer(trainer_id):
    """
    Deletes trainer from database
    - params:
        int: trainer_id
    """
    if "user" not in session or session["user"] != "admin":
        flash("You do not have permission to delete trainer")
        return redirect(url_for("home"))
    else:
        trainer = Trainers.query.get_or_404(trainer_id)
        db.session.delete(trainer)
        db.session.commit()
        return redirect(url_for("manage"))


@app.errorhandler(404)
def handle_bad_request(e):
    '''
    Handles 404 error, page not found
    '''
    return render_template("error404.html")


@app.errorhandler(500)
def internal_error(error):
    '''
    Handles 500 error, internal server error
    '''
    return render_template("error500.html")
