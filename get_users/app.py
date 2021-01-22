from flask import Flask, request, jsonify
import jwt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .models import User, Acl


app = Flask(__name__)
private_key = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/check_user', methods=['GET', 'POST'])
def check_user():

    data = request.get_json()

    if data:
        login = data.get('login', None)
        password = data.get('password', None)
        token = data.get('token', None)

        if token:
            payload = jwt.decode(token, private_key, algorithms=['HS256'])

            res = Acl.query.filter_by(user_id=payload.get('userid', None)).first()

            if res.access_granted:

                user = User.query.filter_by(login=login, password=password)

                if user:
                    return jsonify({'user_id': user.id})

            return jsonify({'error': 'No such user'})

    return jsonify({'error': 'bad token'})


@app.route('/summary', methods=['POST'])
def get_summary_view():
    """
    data = request.get_json()

    if data:

        token = data.get('token', None)

        if token:
            payload = jwt.decode(token, private_key, algorithms=['HS256'])

            return jsonify(get_summary(payload.get('userid', -1)))

    return jsonify({})
    """
    return {'ok'}
