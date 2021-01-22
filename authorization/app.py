from flask import Flask, jsonify, request
import urllib.request
import urllib.parse
from ..appconfig.config import Config
import json
import jwt

app = Flask(__name__)
app.config.from_object(Config)
mstoken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyaWQiOiIxIn0.QVbaPorc1qkWxbc09taz30peQzverFvrWGDPLTQ_7zk"


@app.route('/authorization', methods=['GET', 'POST'])
def index():

    data = request.get_json()

    if data:

        data['token'] = mstoken
        req_data = json.dumps(data).encode("utf-8")
        req = urllib.request.Request(url=app.config['MS_USERS'] + "/check_user", data=req_data, headers={'Content-Type': 'application/json'})

        with urllib.request.urlopen(req) as resp:
            page = resp.read()
            encoding = resp.info().get_content_charset('utf-8')
            answer = json.loads(page.decode(encoding))

            if 'error' in answer:
                return jsonify({'error': answer['error']})

            return jsonify({'userid': answer['user_id'], 'token': get_token(answer['user_id'])})
    return jsonify({"error": "bad data"})


def get_token(userid):

    return jwt.encode({'userid': str(userid)}, app.config['SECRET_KEY'], algorithm='HS256').decode("utf-8")

