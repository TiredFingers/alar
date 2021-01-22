from flask import Flask, jsonify, request
import json
import urllib.request
from ..appconfig.config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import jwt


app = Flask(__name__)
app.config.from_object(Config)
private_key = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///routes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .models import Acl


@app.route('/summary', methods=["POST"])
def get_summary():

    data = request.get_json()

    if data:

        token = data.get('token', None)

        if token:
            payload = jwt.decode(token, private_key, algorithms=['HS256'])
            access = Acl.query.filter_by(user_id=payload['userid']).first()

            if access:
                if access.access_granted:

                    summary_res = []
                    routes = ''

                    url = app.config['MS_USERS'] + '/summary'
                    data = json.dumps({'token': token}).encode('utf-8')
                    r = urllib.request.Request(url=url, data=data, headers={'Content-Type': 'application/json'})

                    with urllib.request.urlopen(r) as resp:
                        page = resp.read()
                        enc = resp.info().get_content_charset('utf-8')
                        users = json.loads(page.decode(enc))

                    url = app.config['MS_ROUTES'] + '/summary'
                    data = json.dumps({'token': token}).encode('utf-8')
                    r = urllib.request.Request(url=url, data=data, headers={'Content-Type': 'application/json'})

                    with urllib.request.urlopen(r) as resp:
                        page = resp.read()
                        enc = resp.info().get_content_charset('utf-8')
                        msroutes_summary = json.loads(page.decode(enc))

                    for user in users:

                        userid = user['id']

                        info = msroutes_summary.get(userid, None)

                        if info:
                            login = user['login']

                            summary_res.append({'userid': userid, 'login': login, 'len': info['total_len'],
                                                'total': info['routes']})

                    return jsonify(summary_res)

    return jsonify({'error': 'no found'})


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
