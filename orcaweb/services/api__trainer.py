import json

import requests

from orcaweb import app


def get__configuration__applications():
    response = requests.get("%s/config/applications" % app.config["ORCA_REWRITE_URL"])
    return json.loads(response.text)


def get__audit():
    response = requests.get("%s/audit" % app.config["ORCA_REWRITE_URL"])
    return json.loads(response.text)


def get__configuration__applications_app(name):
    for app in get__configuration__applications():
        if app["Name"] == name:
            return app
    return None


def set__configuration__applications_app(name, object):
    requests.post("%s/config/applications?application=%s" % (app.config["ORCA_REWRITE_URL"], name), data=json.dumps(object))


def get__configuration__applications_app__config(name):
    response = requests.get("%s/config/applications/configuration/latest?application=%s" % (app.config["ORCA_REWRITE_URL"], name))
    return json.loads(response.text)


def get__status__servers():
    response = requests.get("%s/state" % (app.config["ORCA_REWRITE_URL"]))
    return json.loads(response.text)


def set__configuration__applications_app__config(appName, object):
    requests.post("%s/config/applications/configuration/latest?application=%s" % (app.config["ORCA_REWRITE_URL"], appName), data=json.dumps(object))


def get__configuration__cloud():
    response = requests.get("%s/state/config/cloud" % app.config["ORCA_REWRITE_URL"])
    return json.loads(response.text)


def get__configuration__cloud_state():
    response = requests.get("%s/state/cloud" % app.config["ORCA_REWRITE_URL"])
    return json.loads(response.text)


def set__configuration__cloud(object):
    requests.post("%s/state/config/cloud" % app.config["ORCA_REWRITE_URL"], data=json.dumps(object))


def get__status__application_statistics(application_name):
    response = requests.get(
        "%s/state/cloud/application/performance?application=%s" % (app.config["ORCA_REWRITE_URL"], application_name))
    return json.loads(response.text)


def get__status__application_count(application_name):
    response = requests.get(
        "%s/state/cloud/application/count?application=%s" % (app.config["ORCA_REWRITE_URL"], application_name))
    return json.loads(response.text)


def get__status__application_events(application_name):
    response = requests.get("%s/audit?application=%s" % (app.config["ORCA_REWRITE_URL"], application_name))
    return json.loads(response.text)
