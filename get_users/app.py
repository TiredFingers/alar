from flask import Flask, request, jsonify
from .db import get_user, get_summary
import jwt

app = Flask(__name__)
private_key = 'secret'


@app.route('/check_user', methods=['GET', 'POST'])
def check_user():

    data = request.get_json()

    if data:
        login = data.get('login', None)
        password = data.get('password', None)
        token = data.get('token', None)

        if token:
            payload = jwt.decode(token, private_key, algorithms=['HS256'])

            userid = get_user(login, password, payload['userid'])

            if userid:
                return jsonify({'user_id': userid})

            return jsonify({'error': 'No such user'})

    return jsonify({'error': 'bad token'})


@app.route('/summary', methods=['POST'])
def get_summary_view():

    data = request.get_json()

    if data:

        token = data.get('token', None)

        if token:
            payload = jwt.decode(token, private_key, algorithms=['HS256'])

            return jsonify(get_summary(payload.get('userid', -1)))

    return jsonify({})
