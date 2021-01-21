from flask import Flask, jsonify
from .db import save_to_db
import json
import urllib.request
from appconfig.config import Config


app = Flask(__name__)
app.config.from_object(Config)
mstoken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyaWQiOiJzeXN0ZW0ifQ.bvLIApwfv4c9cjVfQ468M52M58LuxtPM1h_OzVNZdi8"


@app.route('/summary', methods=["GET"])
def get_summary():

    res = dict()

    res['users'] = __get_users_summary()
    res['routes'] = __get_routes_summary()
    res['routes_creation'] = __get_route_creation_summary()
    res['points'] = __get_points_summary()

    save_to_db(res)

    return jsonify(res)


def __get_users_summary():

    req_data = json.dumps({'token': mstoken}).encode('utf-8')
    r = urllib.request.Request(url=app.config['MS_USERS'] + '/summary', data=req_data, headers={'Content-Type': 'application/json'})

    with urllib.request.urlopen(r) as resp:
        page = resp.read()
        enc = resp.info().get_content_charset('utf-8')
        return page.decode(enc)


def __get_routes_summary():
    req_data = json.dumps({'token': mstoken}).encode('utf-8')
    r = urllib.request.Request(url=app.config['MS_ROUTES'] + '/summary', data=req_data, headers={'Content-Type': 'application/json'})

    with urllib.request.urlopen(r) as resp:
        page = resp.read()
        enc = resp.info().get_content_charset('utf-8')
        return page.decode(enc)


def __get_points_summary():
    req_data = json.dumps({'token': mstoken}).encode('utf-8')
    r = urllib.request.Request(url=app.config['MS_POINTS'] + '/summary', data=req_data, headers={'Content-Type': 'application/json'})

    with urllib.request.urlopen(r) as resp:
        page = resp.read()
        enc = resp.info().get_content_charset('utf-8')
        return page.decode(enc)


def __get_route_creation_summary():
    req_data = json.dumps({'token': mstoken}).encode('utf-8')
    r = urllib.request.Request(url=app.config['MS_CREATE_ROUTE'] + '/summary', data=req_data, headers={'Content-Type': 'application/json'})

    with urllib.request.urlopen(r) as resp:
        page = resp.read()
        enc = resp.info().get_content_charset('utf-8')
        return page.decode(enc)
