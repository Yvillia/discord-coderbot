"""
To run please do the following:

$ cd discord-coderbot/
$ pytest -v test/test_api.py

"""

import pytest

# pytest must be run from the main directory for this import to work
from api.app import app, db


@pytest.fixture(scope="module")
def client():
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pytest.db"
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()


def test_ratebot(client):
    data = {"user": "testuser", "rating": 1, "msg": "Hello World!"}
    r = client.post("/ratebot/", json=data)

    assert r.status_code == 200
    assert r.is_json

    if r.status_code and r.is_json:
        assert "msg" in r.json
        if "msg" in r.json:
            assert r.json["msg"] == "Bot rated succesfully"


def test_ratings(client):
    r = client.get("/ratings/")
    assert r.status_code == 200
    assert r.is_json
    if r.status_code and r.is_json:
        assert "ratings" in r.json
        if "ratings" in r.json:
            assert isinstance(r.json["ratings"], list)
            assert r.json["ratings"][0]["user"] == "testuser"
