from flask import Flask, redirect, url_for, session, jsonify, request, render_template
import urllib.request
import urllib.parse
from ..appconfig.config import Config
import json
import random


app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login/<username>", methods=['GET'])
def login(username):

    print()
    print(username)
    print()

    login = username
    password = '123'

    req_data = json.dumps({'login': login, 'password': password}).encode("utf-8")

    r = urllib.request.Request(url=app.config['AUTH_URL'] + "/authorization", data=req_data, headers={'Content-Type': 'application/json'})

    with urllib.request.urlopen(r) as resp:
        page = resp.read()
        encoding = resp.info().get_content_charset('utf-8')
        answer = json.loads(page.decode(encoding))

        if 'error' in answer:
            return jsonify({'error': answer['error']})

        if 'token' in answer:
            session['token'] = answer['token']
            session['userid'] = answer['userid']
            session['username'] = 'user' + str(answer['userid'])

    return redirect(url_for('index'))


@app.route("/points", methods=['GET'])
def get_points():

    url = app.config['MS_POINTS'] + "/points"
    data = json.dumps({'token': session['token']}).encode('utf-8')

    r = urllib.request.Request(url=url, data=data, headers={'Content-Type': 'application/json'})

    with urllib.request.urlopen(r) as resp:
        page = resp.read()
        encoding = resp.info().get_content_charset('utf-8')

        points = json.loads(page.decode(encoding))

    return render_template("points.html", points=points or None)


@app.route("/routes/<userid>", methods=['GET'])
def get_routes(userid):

    routes_url = app.config['MS_ROUTES'] + "/routes"
    data = json.dumps({'token': session['token'], 'owner': userid}).encode('utf-8')

    r = urllib.request.Request(url=routes_url, data=data, headers={'Content-Type': 'application/json'})

    query_points = list()

    with urllib.request.urlopen(r) as resp:
        page = resp.read()
        encoding = resp.info().get_content_charset('utf-8')

        routes = json.loads(page.decode(encoding))

    for route in routes:

        route_points = route.get('points', None)

        if route_points:
            query_points.append(route_points)

    points_url = app.config['MS_POINTS'] + '/points'
    data = json.dumps({'token': session['token'], 'points': query_points}).encode('utf-8')

    r = urllib.request.Request(url=points_url, data=data, headers={'Content-Type': 'application/json'})

    with urllib.request.urlopen(r) as resp:
        page = resp.read()
        encoding = resp.info().get_content_charset('utf-8')
        points = json.loads(page.decode(encoding))

    return render_template("routes.html", routes=routes, points=points)


@app.route("/create_route", methods=['GET'])
def create_route():

    # очевидно, что на момент запроса создания маршрута у авторизованного пользователя на фронте уже будет список точек
    # на основе которых он хочет построить маршрут
    # поэтому здесь нет запроса к микросервису точек
    # в данном случае я просто сгенерировал парочку.

    input_points = list()

    for i in range(10):
        input_points.append(__gen_point(i))

    input_points = json.dumps(input_points)

    from_point = __gen_point(random.randint(1, 10))
    to_point = __gen_point(random.randint(1, 10))

    request_data = json.dumps({'token': session['token'], 'points': input_points, 'from_point': from_point, 'to_point': to_point}).encode('utf-8')
    r = urllib.request.Request(url=app.config['MS_CREATE_ROUTE'] + '/create', data=request_data, headers={'Content-Type': 'application/json'})

    with urllib.request.urlopen(r) as resp:
        page = resp.read()
        encoding = resp.info().get_content_charset('utf-8')
        route = json.loads(page.decode(encoding))

        session['route'] = json.dumps(route)

    return render_template("route.html", route=route)


@app.route('/save_route')
def save_route():

    url = app.config['MS_ROUTES'] + '/route'

    req_data = json.dumps({'token': session['token'], 'route': session['route'], 'name': 'created route name'}).encode('utf-8')

    r = urllib.request.Request(url=url, data=req_data, method='PUT', headers={'Content-Type': 'application/json'})

    with urllib.request.urlopen(r) as resp:
        page = resp.read()
        enc = resp.info().get_content_charset('utf-8')
        return jsonify(json.loads(page.decode(enc)))


@app.route('/summary')
def summary():

    data = json.dumps({'token': session['token']}).encode('utf-8')

    r = urllib.request.Request(url=app.config['MS_SUMMARY'] + '/summary', data=data,
                               headers={"Content-Type": 'application/json'})

    with urllib.request.urlopen(r) as resp:
        page = resp.read()
        enc = resp.info().get_content_charset('utf-8')

        return render_template("summary.html", summary=json.loads(page.decode(enc)))


def __gen_point(id):

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

    name = str(names[random.randint(0, 9)])

    return {str(id): {'coords': str(random.randint(1, 100)) + ':' + str(random.randint(1, 100)),
           'name': name}}

