from flask import Flask, redirect, url_for, session, jsonify, request
import urllib.request
import urllib.parse
from appconfig.config import Config
import json


app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/")
def index():
    return "Hello baby"


@app.route("/login")
def login():

    login = 'test@test.com'
    password = '123'
    data = json.dumps({'login': login, 'password': password}).encode("utf-8")

    r = urllib.request.Request(url=app.config['AUTH_URL'] + "/authorization", data=data, headers={'Content-Type': 'application/json'})

    with urllib.request.urlopen(r) as resp:
        page = resp.read()
        encoding = resp.info().get_content_charset('utf-8')
        answer = json.loads(page.decode(encoding))

        if 'error' in answer:
            return jsonify({'error': answer['error']})

        if 'token' in answer:
            session['token'] = answer['token']
            session['userid'] = answer['userid']

    return redirect(url_for('index'))


@app.route("/points", methods=['GET'])
def get_points():

    url = app.config['MS_POINTS'] + "/points"
    data = json.dumps({'token': session['token']}).encode('utf-8')

    r = urllib.request.Request(url=url, data=data, headers={'Content-Type': 'application/json'})

    with urllib.request.urlopen(r) as resp:
        page = resp.read()
        encoding = resp.info().get_content_charset('utf-8')

        return jsonify(json.loads(page.decode(encoding)))


@app.route("/routes", methods=['GET'])
def get_routes():

    routes_url = app.config['MS_ROUTES'] + "/routes"
    data = json.dumps({'token': session['token']}).encode('utf-8')

    r = urllib.request.Request(url=routes_url, data=data, headers={'Content-Type': 'application/json'})

    query_points = list()

    with urllib.request.urlopen(r) as resp:
        page = resp.read()
        encoding = resp.info().get_content_charset('utf-8')

        routes = json.loads(page.decode(encoding))

    for k in routes.keys():
        route = routes[k]

        route_points = route.get('route', None)

        if route_points:
            query_points.append(route_points)

    points_url = app.config['MS_POINTS'] + '/points'
    data = json.dumps({'token': session['token'], 'points': query_points}).encode('utf-8')

    r = urllib.request.Request(url=points_url, data=data, headers={'Content-Type': 'application/json'})

    with urllib.request.urlopen(r) as resp:
        page = resp.read()
        encoding = resp.info().get_content_charset('utf-8')
        points = json.loads(page.decode(encoding))

    return jsonify({'routes': routes, 'points': points})


@app.route("/create_route")
def create_route():

    # очевидно, что на момент запроса создания маршрута у авторизованного пользователя на фронте уже будет список точек
    # на основе которых он хочет построить маршрут
    # поэтому здесь нет запроса к микросервису точек

    input_data = request.get_json()

    if input_data:

        points = input_data.get('points', {})
        from_point = input_data.get('from_point', {})
        to_point = input_data.get('to_point', {})

        request_data = json.dumps({'token': session['token'], 'points': points, 'from_point': from_point, 'to_point': to_point}).encode('utf-8')
        r = urllib.request.Request(url=app.config['MS_CREATE_ROUTE'] + '/create', data=request_data, headers={'Content-Type': 'application/json'})

        with urllib.request.urlopen(r) as resp:
            page = resp.read()
            encoding = resp.info().get_content_charset('utf-8')
            return jsonify(page.decode(encoding))

    else:
        return jsonify({'error': 'not found'})
