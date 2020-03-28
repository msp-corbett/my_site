from app.test.fixtures import app, client  # noqa

def test_app_index(app, client):  # noqa
    with client:
        resp = client.get("/")
        assert resp.status_code == 200