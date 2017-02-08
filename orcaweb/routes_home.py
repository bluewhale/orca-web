import re
import uuid

import flask
from flask import render_template
from flask import request
from flask import redirect

from orcaweb import app
from orcaweb.services import api__trainer


@app.route("/")
def route_dashboard():
    return render_template("dashboard.html", configuration=api__trainer.get__configuration__applications())


@app.route("/servers")
def route_servers():
    return render_template("servers.html")


@app.route("/applications")
def route_applications_get():
    return flask.jsonify(applications=api__trainer.get__configuration__applications())


@app.route("/audit")
def route_audit():
    return render_template("audit.html", audit=api__trainer.get__audit())


@app.route("/settings")
def route_settings():
    return render_template("settings.html", cloud=api__trainer.get__configuration__cloud())


@app.route("/ajax/settings", methods=["GET"])
def ajax__route_settings():
    return flask.jsonify(api__trainer.get__configuration__cloud())

@app.route("/ajax/servers", methods=["GET"])
def ajax__route_servers():
    servers = api__trainer.get__status__servers()
    ret = []
    for server in servers.values():
        ret.append(server)
    return flask.jsonify(servers=ret)


@app.route("/ajax/settings", methods=["POST"])
def ajax__route_settings_post():
    api__trainer.set__configuration__cloud(request.json)
    return ""

@app.route("/ajax/application/<name>", methods=["GET"])
def ajax__route_application(name):
    return flask.jsonify(api__trainer.get__configuration__applications_app(name))

@app.route("/ajax/application/<name>/configuration", methods=["GET"])
def ajax__route_application_configuration(name):
    return flask.jsonify(api__trainer.get__configuration__applications_app__config(name))


@app.route("/ajax/application/<name>", methods=["POST"])
def ajax__route_application_post(name):
    api__trainer.set__configuration__applications_app(name, request.json)
    return ""


@app.route("/ajax/application/<name>/configuration", methods=["POST"])
def ajax__route_application_post_configuration(name):
    api__trainer.set__configuration__applications_app__config(name, request.json)
    return ""


@app.route("/settings", methods=["POST"])
def route_settings_save():
    cloud_provider_configuration = {
        "Type": request.form.get("Type"),
        "MinInstances": int(request.form.get("MinInstances")),
        "MaxInstances": int(request.form.get("MaxInstances"))
    }

    if cloud_provider_configuration["Type"] == "AWS":
        cloud_provider_configuration["AWSConfiguration"] = {
            "Key": request.form.get("Key"),
            "Secret": request.form.get("Secret"),
            "Region": request.form.get("Region"),
            "AMI": request.form.get("AMI"),
            "SecurityGroupId": request.form.get("SecurityGroupId")
        }

    api__trainer.set__configuration__cloud(cloud_provider_configuration)
    return redirect("/settings")


@app.route("/application/<name>/scaling", methods=["GET"])
def route_application_scaling(name):
    return render_template("application_settings.html", name=name)

@app.route("/application/<name>/configuration", methods=["GET"])
def route_application_configuration(name):
    return render_template("application_configuration.html", name=name)


@app.route("/application/<name>/events", methods=["GET"])
def route_application_events(name):
    return render_template("application_events.html", name=name)


@app.route("/application/<name>/server/<serverid>", methods=["GET"])
def route_application_server(name, serverid):
    return render_template("application_server.html", name=name, serverid=serverid)


@app.route("/application/<name>/overview", methods=["GET"])
def route_application_overview(name):
    return render_template("application_overview.html", name=name)


@app.route("/ajax/application/<name>/servers", methods=["GET"])
def ajax__route_application_servers(name):
    servers = []
    cloud_layout = api__trainer.get__configuration__cloud_state()
    for hostid, server in cloud_layout["Current"]["Layout"].items():
        for name, application in server["Apps"].items():
            if name == name:
                servers.append(server)
    return flask.jsonify(servers=servers)


@app.route("/ajax/application/<name>/servers/desired", methods=["GET"])
def ajax__route_application_servers_desired(name):
    servers = []
    cloud_layout = api__trainer.get__configuration__cloud_state()
    for hostid, server in cloud_layout["Desired"]["Layout"].items():
        for name, application in server["Apps"].items():
            if name == name:
                servers.append(server)
    return flask.jsonify(servers=servers)


@app.route("/ajax/application/<name>/servers/memory", methods=["GET"])
def ajax__route_application_servers_memory(name):
    return flask.jsonify(memory=api__trainer.get__status__application_statistics(name))


@app.route("/ajax/application/<name>/count", methods=["GET"])
def ajax__route_application_count(name):
    return flask.jsonify(count=api__trainer.get__status__application_count(name))


@app.route("/ajax/application/<name>/events", methods=["GET"])
def ajax__route_application_events(name):
    return flask.jsonify(events=api__trainer.get__status__application_events(name))

def extract_command(string_command):
    p = re.compile('([a-z]+)\s(.*)')
    m = p.match(string_command)
    return m.group(1).strip(), m.group(2).strip()


@app.route("/application", methods=["POST"])
def route_application__add():
    application = request.json
    api__trainer.set__configuration__applications_app(application["Name"], application)
    return ""


@app.route("/application/<name>", methods=["POST"])
def route_application__set(name):
    existing_configuration = api__trainer.get__configuration__applications_app(name)
    existing_configuration["Type"] = request.form.get("Type")

    existing_configuration["TargetDeploymentCount"] = int(request.form.get("TargetDeploymentCount"))
    existing_configuration["MinDeploymentCount"] = int(request.form.get("MinDeploymentCount"))

    existing_configuration["DockerConfig"]["Tag"] = request.form.get("Tag")
    existing_configuration["DockerConfig"]["Repository"] = request.form.get("Repository")
    existing_configuration["DockerConfig"]["Reference"] = request.form.get("Reference")

    existing_configuration["Needs"]["MemoryNeeds"] = int(request.form.get("MemoryNeeds"))
    existing_configuration["Needs"]["CpuNeeds"] = int(request.form.get("CpuNeeds"))
    existing_configuration["Needs"]["NetworkNeeds"] = int(request.form.get("NetworkNeeds"))

    existing_configuration["LoadBalancer"] = request.form.get("LoadBalancer")
    existing_configuration["Network"] = request.form.get("Network")

    api__trainer.set__configuration__applications_app(existing_configuration)
    return flask.redirect("/application/" + name)


@app.route("/application/<name>/configuration", methods=["POST"])
def route_application__set_configuration(name):
    existing_configuration = api__trainer.get__configuration__applications_app__config(name)
    existing_configuration["DockerConfig"]["Tag"] = request.form.get("Tag")
    existing_configuration["DockerConfig"]["Repository"] = request.form.get("Repository")
    existing_configuration["DockerConfig"]["Reference"] = request.form.get("Reference")

    existing_configuration["Needs"]["MemoryNeeds"] = int(request.form.get("MemoryNeeds"))
    existing_configuration["Needs"]["CpuNeeds"] = int(request.form.get("CpuNeeds"))
    existing_configuration["Needs"]["NetworkNeeds"] = int(request.form.get("NetworkNeeds"))

    existing_configuration["LoadBalancer"] = request.form.get("LoadBalancer")
    existing_configuration["Network"] = request.form.get("Network")

    api__trainer.set__configuration__applications_app__config(name, existing_configuration)
    return flask.redirect("/application/" + name)
