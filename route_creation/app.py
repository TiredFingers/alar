from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)
private_key = 'secret'
acl = {
    '0': True,
    '1': True
}


@app.route("/create", methods=['POST'])
def create_route():
    data = request.get_json()

    if data:
        token = data.get('token', None)

        if token:
            payload = jwt.decode(token, private_key, algorithms=['HS256'])

            userid = payload.get('userid', None)

            if acl.get(userid, None):

                points = data.get('points', None)
                from_point = data.get('from_point', None)
                to_point = data.get('to_point', None)

                if points:
                    return jsonify(__calc_route(points, from_point, to_point))

    return jsonify({'error': 'not found'})


@app.route('/summary', methods=['GET'])
def summary():
    data = request.get_json()

    if data:

        token = data.get('token', None)

        if token:
            payload = jwt.decode(token, private_key, algorithms=['HS256'])

            return jsonify(__get_summary(payload.get('userid', -1)))

    return jsonify({})


def __calc_route(points, from_point, to_point):
    #делает расчёты
    #возвращает точки маршрута

    return [
        {
            '0': {
                'l': 55.755814,
                'a': 37.617635,
                'name': 'Moscow'
            }
        },
        {
            '1': {
                'l': 48.856663,
                'a': 2.351556,
                'name': 'Paris'
            }
        }
    ]


def __get_summary(userid):
    granted = acl.get(userid, None)

    if granted:
        return {'created': '20000'}
    return {}
