import pytest
from app.test.fixtures import client

def test_health(client):
    resp = client.get('/health')
    assert resp.status_code == 200
    assert resp.is_json
    assert resp.json == "healthy"