import pytest
import requests
import json
from app.test.fixtures import  new_app, client


def test_user_get(client):
    resp = client.get('/api/user')
    assert resp.status_code == 200
    assert resp.is_json
    assert resp.json[0]['ID'] == 1


def test_user_post(client):
    body = {
        "FirstName": "Test",
        "LastName": "Test",
        "UserName": "Test",
        "Email": "Test@my-site.com"
    }

    resp = client.post(
        '/api/user',
        json=body)

    assert resp.status_code == 200


def test_user_put(client):
    pass


def test_user_patch(client):
    patch = [
        {
            "op": "replace",
            "path": 'FirstName',
            "value": 'Patch'
        }
    ]

    resp = client.patch('/api/user/3', json=patch)
    assert resp.status_code == 200


def test_user_delete(client):
    resp = client.delete('/api/user/3')

    assert resp.status_code == 200