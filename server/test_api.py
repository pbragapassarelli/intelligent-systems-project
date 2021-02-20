from api import app
from flask import json

def test_hello():
    response = app.test_client().post(
        "/hello",
        data=json.dumps({ "name": "42" }),
        content_type="application/json"
    )

    assert response.status_code == 400


def test_hello2():
    response = app.test_client().post(
        "/hello",
        data=json.dumps({ "name": "Willian" }),
        content_type="application/json"
    )

    assert response.status_code == 200