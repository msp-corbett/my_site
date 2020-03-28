""" Fixtures to be available testing-wide """
# Testing follows setup from 'flaskerize'
# see: https://flaskerize.readthedocs.io/en/latest/
#      http://alanpryorjr.com/2019-05-20-flask-api-example/
#      https://github.com/apryor6/flask_api_example
import pytest
from app import create_app


@pytest.fixture
def app():
    """ The app with Testing config variables """
    return create_app("test")


@pytest.fixture
def client(app):
    """ The test client to work in """
    return app.test_client()