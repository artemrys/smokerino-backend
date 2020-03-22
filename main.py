import flask

from functions.smokerino import add_cigarette
from functions.smokerino import get_cigarette


def add_cigarette_request(request: flask.Request):
    return add_cigarette(request)


def get_cigarette_request(request: flask.Request):
    return get_cigarette(request)
