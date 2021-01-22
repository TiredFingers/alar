from flask import Flask, request, jsonify
import jwt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
private_key = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .models import User, Acl


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

            if res:

                user = User.query.filter_by(login=login, password=password).first()

                if user:
                    return jsonify({'user_id': user.id})

            return jsonify({'error': 'No such user'})

    return jsonify({'error': 'bad token'})


@app.route('/summary', methods=['POST'])
def get_users():
    data = request.get_json()

    if data:
        token = data.get('token', None)

        if token:
            payload = jwt.decode(token, private_key, algorithms=['HS256'])

            res = Acl.query.filter_by(user_id=payload.get('userid', None)).first()

            if res:
                if res.access_granted:

                    users = list()

                    for user in User.query.all():
                        users.append({'id': str(user.id), 'login': user.login})

                    return jsonify(users)

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

    db.session.add(User(login='user1', password='123'))
    db.session.add(User(login='user2', password='123'))
    db.session.add(User(login='user3', password='123'))

    db.session.commit()

    return "Filled"


@app.route("/delete_all")
def delete_data():

    Acl.query.delete()
    User.query.delete()
    return "Deleted"
