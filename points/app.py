from flask import Flask, request, jsonify
from .db import get_points, get_summary
import jwt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
private_key = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///points.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/points', methods=["POST"])
def get_points_view():

    data = request.get_json()

    if data:
        token = data.get('token', None)

        if token:
            payload = jwt.decode(token, private_key, algorithms=['HS256'])
            points = get_points(userid=payload['userid'])

            if points:
                return jsonify(points)

    return jsonify({'error': 'Not found'})


@app.route('/summary', methods=['GET'])
def summary():
    data = request.get_json()

    if data:

        token = data.get('token', None)

        if token:
            payload = jwt.decode(token, private_key, algorithms=['HS256'])

            return jsonify(get_summary(payload.get('userid', -1)))

    return jsonify({})
