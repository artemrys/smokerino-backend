from unittest.mock import Mock

import flask
import pytest

import main


# Create a fake "app" for generating test request contexts.
@pytest.fixture(scope="module")
def app():
    return flask.Flask(__name__)


@pytest.mark.parametrize("method", ["POST", "PUT", "DELETE"])
def test_get_cigarette_returns_not_allowed_if_not_get_request(app, method):
    request_mock = Mock(method=method)
    with app.test_request_context():
        response = main.get_cigarette_request(request_mock)
    assert response.status_code == 405


@pytest.mark.parametrize("method", ["GET", "PUT", "DELETE"])
def test_add_cigarette_returns_not_allowed_if_not_post_request(app, method):
    request_mock = Mock(method=method)
    with app.test_request_context():
        response = main.add_cigarette_request(request_mock)
    assert response.status_code == 405
