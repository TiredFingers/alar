from flask import Flask, request, jsonify
from .db import get_points, get_summary
import jwt

app = Flask(__name__)
private_key = 'secret'


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
