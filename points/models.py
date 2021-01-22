from .app import db


class Point(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float)
    longtitude = db.Column(db.Float)
    name = db.Column(db.String)


class Acl(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    access_granted = db.Column(db.Boolean)
