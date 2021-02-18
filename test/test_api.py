## Backend API must be running
# to run HTTP API local`host server run the following in another terminal
# python api/app.py

import requests
import pytest
import json

server_url = "http://localhost:5000"


def test_connection():
    r = requests.get(server_url + "/")
    assert r.json()


def test_adduser():
    headers = {"content-type": "application/json"}
    data = {"email": "testuser@test.com", "username": "testuser"}
    r = requests.post(server_url + "/adduser", headers=headers, data=json.dumps(data))
    assert r.json()["msg"] == "user added"


def test_getusers():
    r = requests.get(server_url + "/getusers/")
    r_json = r.json()
    assert r_json is not None
    if r_json is not None:
        assert isinstance(r_json["users"], list)


def test_getusername():
    r = requests.get(server_url + "/getusername/?email=testuser@test.com")
    r_json = r.json()
    assert r_json is not None
    if r_json is not None:
        assert r_json["username"] == "testuser"


def test_deluser():
    headers = {"content-type": "application/json"}
    data = {"username": "testuser"}
    r = requests.post(server_url + "/deluser", headers=headers, data=json.dumps(data))
    assert r.json()["msg"] == "user deleted"
