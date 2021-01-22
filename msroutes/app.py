from flask import Flask, request, jsonify
import jwt
from ..appconfig.config import Config
from .db import get_routes, get_summary
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)
private_key = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///routes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route("/routes", methods=["POST"])
def get_routes_view():
    """
    all routes of all users
    """

    data = request.get_json()

    if data:
        token = data.get('token', None)

        if token:
            payload = jwt.decode(token, private_key, algorithms=['HS256'])

            userid = payload.get('userid', None)

            if userid:
                return jsonify(get_routes(userid))

    return jsonify({'error': 'not found'})


@app.route("/route/<int:userid>", methods=['GET'])
def get_user_route(userid):
    pass


@app.route("/route", methods=["PUT"])
def save_route():
    pass


@app.route('/summary', methods=['POST'])
def get_summary():
    data = request.get_json()

    if data:

        token = data.get('token', None)

        if token:
            payload = jwt.decode(token, private_key, algorithms=['HS256'])

            return jsonify(get_summary(payload.get('userid', -1)))

    return jsonify({})
