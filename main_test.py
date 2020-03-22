from unittest import mock

import flask
import pytest
from google.cloud import firestore

import main


# Create a fake "app" for generating test request contexts.
@pytest.fixture(scope="module")
def app():
    return flask.Flask(__name__)


@pytest.fixture(scope="function")
def firestore_client():
    mock_firestore_client = mock.MagicMock(firestore.Client)
    build_firestore_client_patcher = mock.patch(
        "functions.smokerino.build_firestore_client",
        return_value=mock_firestore_client)
    build_firestore_client_patcher.start()
    yield build_firestore_client_patcher
    build_firestore_client_patcher.stop()


@pytest.mark.parametrize("method", ["POST", "PUT", "DELETE"])
def test_get_cigarette_returns_not_allowed_if_not_get_request(app, method):
    request_mock = mock.Mock(method=method)
    with app.test_request_context():
        response = main.get_cigarette_request(request_mock)
    assert response.status_code == 405


def test_get_cigarette_returns_bad_request_when_no_user_id(
        app, firestore_client):
    request_mock = mock.Mock(method="GET", args={})
    with app.test_request_context():
        response = main.get_cigarette_request(request_mock)
    assert response.status_code == 400


@pytest.mark.parametrize("method", ["GET", "PUT", "DELETE"])
def test_add_cigarette_returns_not_allowed_if_not_post_request(app, method):
    request_mock = mock.Mock(method=method)
    with app.test_request_context():
        response = main.add_cigarette_request(request_mock)
    assert response.status_code == 405


def test_add_cigarette_returns_bad_request_when_no_user_id(
        app, firestore_client):
    request_mock = mock.Mock(method="POST", args={})
    with app.test_request_context():
        response = main.add_cigarette_request(request_mock)
    assert response.status_code == 400
