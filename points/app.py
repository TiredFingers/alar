from flask import Flask, request, jsonify
import jwt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import random

app = Flask(__name__)
private_key = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///points.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .models import Acl, Point


@app.route('/points', methods=["POST"])
def get_points_view():

    data = request.get_json()

    if data:
        token = data.get('token', None)

        if token:
            payload = jwt.decode(token, private_key, algorithms=['HS256'])

            access = Acl.query.filter_by(user_id=payload['userid']).first()

            if access:
                if access.access_granted:

                    res = []

                    for point in Point.query.all():
                        res.append({point.id: {'coords': str(point.latitude) + ':' + str(point.longtitude),
                                               'name': point.name}})

                    return jsonify(res)

    return jsonify({'error': 'Not found'})


@app.route('/create_schema')
def create_schema():
    db.create_all()
    return "Created"


@app.route("/fill_db")
def fill_db():

    db.session.add(Acl(user_id=1, access_granted=True))
    db.session.add(Acl(user_id=2, access_granted=True))
    db.session.add(Acl(user_id=3, access_granted=True))
    db.session.add(Acl(user_id=4, access_granted=False))

    names = {
        0: 'Moscow',
        1: 'Saint Petersburg',
        2: 'Novgorod',
        3: 'Kazan',
        4: 'Tver',
        5: 'Krasnodar',
        6: 'Kiev',
        7: 'Minsk',
        8: 'Astrahan',
        9: 'Shpak flat =)'
    }

    for i in range(100):
        name = str(names[random.randint(0, 9)])
        db.session.add(Point(latitude=random.randint(1, 100) * 1.12383,
                                          longtitude=random.randint(1, 100) * 1.12383, name=name))

    db.session.commit()

    return "Filled"


@app.route("/delete_all")
def delete_data():

    Acl.query.delete()
    Point.query.delete()
    return "Deleted"
