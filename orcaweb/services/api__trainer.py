import json

import requests


def get__configuration__applications():
    response = requests.get("http://localhost:5000/state/config/applications")
    return json.loads(response.text)


def get__configuration__applications_app(name):
    return get__configuration__applications()[name]


def set__configuration__applications_app(object):
    requests.post("http://localhost:5000/state/config/applications", data=json.dumps(object))
