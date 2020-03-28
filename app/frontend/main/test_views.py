import pytest
from app.test.fixtures import new_app, client

def test_index(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'Welcome home' in resp.data