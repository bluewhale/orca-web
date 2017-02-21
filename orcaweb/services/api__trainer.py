import json

import requests
from flask.ext.login import current_user

from orcaweb import app


class NoSession(Exception):
    def __init__(self, message, *args, **kwargs):
        super(NoSession, self).__init__(*args, **kwargs)
        self.message = message


def __authenticated_get_request(uri):
    from orcaweb.routes_base import session__get_hostname

    response = requests.get("%s/%s&token=%s" % (session__get_hostname(), uri, current_user.get_id()))
    if response.status_code == 403:
        raise NoSession("Invalid or no session")
    return json.loads(response.text)


def __authenticated_post_request(uri, data):
    from orcaweb.routes_base import session__get_hostname

    response = requests.post("%s/%s&token=%s" % (session__get_hostname(), uri, current_user.get_id()), data=data)
    if response.status_code == 403:
        raise NoSession("Invalid or no session")
    return json.loads(response.text)


def authenticate(hostname, username, password):
    response = requests.get("%s/authenticate?username=%s&password=%s" % (hostname, username, password))
    if response.status_code == 200:
        response_object = json.loads(response.text)
        return response_object["Token"]
    return None


def get__configuration__applications():
    response = __authenticated_get_request("config/applications?")
    return response


def get__audit(search="", limit="100"):
    return __authenticated_get_request("state/cloud/audit?&search=%s&limit=%s" % (search, limit))


def get__configuration__applications_app(name):
    for app in get__configuration__applications():
        if app["Name"] == name:
            return app
    return None


def set__configuration__applications_app(name, object):
    __authenticated_post_request("config/applications?application=%s" % (name), data=json.dumps(object))


def get__configuration__applications_app__config(name):
    response = __authenticated_get_request("config/applications/configuration/latest?application=%s" % (name))
    return response


def get__status__servers():
    response = __authenticated_get_request("state?")
    return response


def set__configuration__applications_app__config(appName, object):
    __authenticated_post_request("config/applications/configuration/latest?application=%s" % (appName),
                                 data=json.dumps(object))


def get__configuration__cloud():
    response = __authenticated_get_request("state/config/cloud?")
    return response

def get__settings():
    response = __authenticated_get_request("settings?")
    return response


def get__configuration__cloud_state():
    response = __authenticated_get_request("state/cloud?")
    return response

def get__status__server(name):
    response = __authenticated_get_request("state?")[name]
    return response


def set__configuration__cloud(object):
    __authenticated_post_request("state/config/cloud?", data=json.dumps(object))

def set__properties(object):
    __authenticated_post_request("properties?", data=json.dumps(object))

def get__properties():
    properties = []
    for value in __authenticated_get_request("properties?").itervalues():
        properties.append(value)
    return properties

def get__properties_by_name(name):
    return __authenticated_get_request("properties?")[name]

def set__settings(object):
    __authenticated_post_request("settings?", data=json.dumps(object))


def get__status__application_statistics(application_name):
    response = __authenticated_get_request("state/cloud/application/performance?application=%s" % (application_name))
    return response


def get__status__application_count(application_name):
    response = __authenticated_get_request("state/cloud/application/count?application=%s" % (application_name))
    return response


def get__status__application_events(application_name, search="", limit="100"):
    response = __authenticated_get_request("state/cloud/application/audit?application=%s&search=%s&limit=%s" % (application_name, search, limit))
    return response


def get__status__application_logs(application_name, search="", limit="100"):
    response = __authenticated_get_request("state/cloud/application/logs?application=%s&search=%s&limit=%s" % (application_name, search, limit))
    return response

def get__status__server_logs(server, search="", limit="100"):
    response = __authenticated_get_request("state/cloud/host/logs?host=%s&search=%s&limit=%s" % (server, search, limit))
    return response

def get__status__server_audit(server, search="", limit="100"):
    response = __authenticated_get_request("state/cloud/host/audit?host=%s&search=%s&limit=%s" % (server,search, limit))
    return response

def get__status__server_memory(server):
    response = __authenticated_get_request("state/cloud/host/performance?host=%s" % (server))
    return response

def get__status__application_server_memory(server, application):
    response = __authenticated_get_request("state/cloud/application/host/performance?host=%s&application=%s" % (server, application))
    return response

