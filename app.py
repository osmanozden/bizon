from datetime import date
from flask import Flask
from flask import abort
from flask import g
from flask import jsonify
from flask import request
from flask import url_for as flask_url_for
from flask.json import JSONEncoder
from flask_cors import CORS, cross_origin
from flask_login import LoginManager
from time import time
from flask_mail import Mail, Message


import logging

class MyJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, date):
            return o.isoformat()
        return super().default(o)

class MyFlask(Flask):
    json_encoder = MyJSONEncoder

app = MyFlask(__name__)

CORS(app)

