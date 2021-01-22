from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import jwt
import random
import json


app = Flask(__name__)
private_key = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///route_creation.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .models import Acl


@app.route("/create", methods=['POST'])
def create_route():
    data = request.get_json()

    if data:
        token = data.get('token', None)

        if token:
            payload = jwt.decode(token, private_key, algorithms=['HS256'])

            access = Acl.query.filter_by(user_id=payload.get('userid', None)).first()

            if access:
                if access.access_granted:

                    points = json.loads(data.get('points', None))
                    from_point = data.get('from_point', None)
                    to_point = data.get('to_point', None)

                    if points is None:
                        return jsonify({'error': 'no points'})

                    return jsonify(__calc_route(points, from_point, to_point))

    return jsonify({'error': 'not found'})


@app.route('/summary', methods=['GET'])
def summary():
    data = request.get_json()

    if data:

        token = data.get('token', None)

        if token:
            payload = jwt.decode(token, private_key, algorithms=['HS256'])

            return jsonify({'created': 100500})

    return jsonify({})


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

    db.session.commit()

    return "Filled"


@app.route("/delete_all")
def delete_data():

    Acl.query.delete()
    return "Deleted"


def __calc_route(points, from_point, to_point):

    if points is None:
        return []

    res = list()
    # fastest route ever =)
    res.append(from_point)
    for i in range(8):
        res.append(points.pop(random.randint(0, len(points)-2)))
    res.append(to_point)

    return res
