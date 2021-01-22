from flask import Flask, request, jsonify
import jwt
from ..appconfig.config import Config
from .db import get_routes, get_summary
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
import random


app = Flask(__name__)
app.config.from_object(Config)
private_key = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///routes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .models import Acl, Route


@app.route("/routes", methods=["POST"])
def get_routes_view():

    data = request.get_json()

    if data:
        token = data.get('token', None)

        if token:
            payload = jwt.decode(token, private_key, algorithms=['HS256'])

            userid = payload.get('userid', None)

            if userid:

                access = Acl.query.filter_by(user_id=userid).first()

                if access.access_granted:

                    routes = []

                    res = Route.query.filter_by(user_id=data.get('owner', None))

                    if res:
                        for route in res:
                            routes.append({route.id: {'owner': route.user_id, 'points': route.points, 'name': route.name, 'length': route.length}})

                    return jsonify(routes)

    return jsonify({'error': 'not found'})


@app.route("/summary", methods=['POST'])
def get_routes():
    data = request.get_json()

    if data:
        token = data.get('token', None)

        if token:
            payload = jwt.decode(token, private_key, algorithms=['HS256'])

            res = Acl.query.filter_by(user_id=payload.get('userid', None)).first()

            if res:
                if res.access_granted:

                    from sqlalchemy import func

                    res = dict()

                    for route, route_len, routes in Route.query.add_columns(func.sum(Route.length), func.count(Route.name)).group_by(Route.user_id).all():
                        res[str(route.user_id)] = {'total_len': route_len, 'routes': routes}

                    return jsonify(res)

    return jsonify({'error': 'not found'})


@app.route("/route", methods=["PUT"])
def save_route():

    data = request.get_json()

    if data:
        token = data.get('token', None)

        if token:
            payload = jwt.decode(token, private_key, algorithms=['HS256'])
            userid = payload.get('userid', None)

            if userid:
                access = Acl.query.filter_by(user_id=userid).first()

                if access.access_granted:
                    db.session.add(Route(user_id=userid, points=data.get('points', None), name=data.get('name', None),
                                         length=random.randint(100, 100000)))
                    db.session.commit()

                    return jsonify({'status': 'created'})

    return jsonify({'error': 'not found'})


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

    for i in range(10):
        points = str(json.dumps([p for p in range(random.randint(1, 100))]).encode('utf-8'))
        name = str(names[random.randint(0, 9)] + ' to ' + names[random.randint(0, 9)])
        db.session.add(Route(user_id=random.randint(2, 4), points=points, name=name, length=random.randint(10, 3000)))

    db.session.commit()

    return "Filled"


@app.route("/delete_all")
def delete_data():

    Acl.query.delete()
    Route.query.delete()
    return "Deleted"
