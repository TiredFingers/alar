from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Acl(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    access_granted = db.Column(db.Boolean)


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.Text)
    password = db.Column(db.Text)
