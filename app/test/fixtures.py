""" Fixtures to be available testing-wide """
# Testing follows setup from 'flaskerize'
# see: https://flaskerize.readthedocs.io/en/latest/
#      http://alanpryorjr.com/2019-05-20-flask-api-example/
#      https://github.com/apryor6/flask_api_exampleimport pytest
import pytest
from app import create_app

new_app = create_app('test')

@pytest.fixture
def client():
    client = new_app.test_client()
    return client
