from .app import db


class Acl(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    access_granted = db.Column(db.Boolean)


class Route(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    points = db.Column(db.Text)  # json points
    name = db.Column(db.Text)
