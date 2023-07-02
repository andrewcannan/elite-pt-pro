from eliteptpro import db


class User(db.Model):
    # schema for User model
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=True)
    password = db.Column(db.String, unique=True, nullable=True)
    is_pt = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        # represents itself in the form of a string
        return f"{self.id} - {self.username} | PT: {self.is_pt}"


class Trainers(db.Model):
    # schema for Trainers model
    id = db.Column(db.Integer, primary_key=True)
    trainer_name = db.Column(db.String, nullable=False)
    holidays = db.relationship(
        "Holidays", backref="trainers", cascade="all, delete", lazy=True)
    sessions = db.relationship(
        "Sessions", backref="trainers", cascade="all, delete", lazy=True)

    def __repr__(self):
        # represents itself in the form of a string
        return self.trainer_name


class Holidays(db.Model):
    # schema for Holidays model
    id = db.Column(db.Integer, primary_key=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey(
            "trainers.id", ondelete="CASCADE"), nullable=False)
    date = db.Column(db.Date, unique=True, nullable=False)

    def __repr__(self):
        # represents itself in the form of a string
        return self.date


class Sessions(db.Model):
    # schema for Sessions model
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    trainer_id = db.Column(db.Integer, db.ForeignKey(
        "trainers.id", ondelete="CASCADE"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        # represents itself in the form of a string
        return f"{self.id} - Date: {self.date} | Time: {self.time}"