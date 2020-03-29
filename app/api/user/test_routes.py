import pytest
from app.test.fixtures import  new_app, client


def test_user_get(client):
    resp = client.get('/api/user')
    assert resp.status_code == 200
    assert resp.is_json
    assert resp.json[0]['id'] == 1