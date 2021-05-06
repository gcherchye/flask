"""Simple example"""
from __future__ import absolute_import

from flask import Flask
from flask.helpers import make_response


app = Flask(__name__)

@app.route('/')
def index():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '42')

    return response

@app.route('/user/<id>')
def get_user(name):
    return f'<h1>Hello {name} ! </h1>'