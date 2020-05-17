from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    notes = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Substance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    fiz = db.Column(db.String(64))
    fiz2 = db.Column(db.String(64))
    put = db.Column(db.String(64))
    put2 = db.Column(db.String(64))
    put3 = db.Column(db.String(64))
    put4 = db.Column(db.String(64))
    kli = db.Column(db.String(64))
    kli2 = db.Column(db.String(64))
    kli3 = db.Column(db.String(64))
    kli4 = db.Column(db.String(64))
    kli5 = db.Column(db.String(64))
    kli6 = db.Column(db.String(64))
    kli7 = db.Column(db.String(64))
    kli8 = db.Column(db.String(64))
    kli9 = db.Column(db.String(64))
    kli10 = db.Column(db.String(64))

    def __repr__(self):
        return '<Substance {}>'.format(self.title)
