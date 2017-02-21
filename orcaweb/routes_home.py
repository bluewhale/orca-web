import re
import uuid

import flask
from flask import render_template
from flask import request
from flask import redirect
from flask.ext.login import login_required

from orcaweb import app
from orcaweb.services import api__trainer


@app.route("/")
@login_required
def route_dashboard():
    return render_template("dashboard.html", configuration=api__trainer.get__configuration__applications())


@app.route("/servers")
@login_required
def route_servers():
    return render_template("servers.html")


@app.route("/applications")
@login_required
def route_applications_get():
    return flask.jsonify(applications=api__trainer.get__configuration__applications())


@app.route("/ajax/applications/by/vpc")
@login_required
def route_applications_get__by_vpc():
    ret = []
    servers = api__trainer.get__status__servers()
    applications = api__trainer.get__configuration__applications()
    for app in applications:
        app["Running"] = 0
        app["Failed"] = 0

        for key, server in servers.iteritems():
            if server.get("Apps"):
                for serverAppState in server.get("Apps", []):
                    if serverAppState["Name"] == app["Name"]:
                        if serverAppState["State"] == "running":
                            app["Running"] += 1
                        else:
                            app["Failed"] += 1

        if app["Enabled"]:
            if app["Running"] == app["DesiredDeployment"]:
                app["Status"] = "Ok"

            if app["Running"] != app["DesiredDeployment"]:
                app["Status"] = "Scaling"
        else:
            app["Status"] = "Disabled"
        ret.append(app)

    return flask.jsonify(applications=ret)


@app.route("/audit")
@login_required
def route_audit():
    return render_template("events.html")


@app.route("/settings")
@login_required
def route_settings():
    return render_template("settings.html")


@app.route("/ajax/settings", methods=["GET"])
@login_required
def ajax__route_settings():
    return flask.jsonify(api__trainer.get__settings())


@app.route("/ajax/servers", methods=["GET"])
@login_required
def ajax__route_servers():
    servers = api__trainer.get__status__servers()
    ret = []
    for server in servers.values():
        ret.append(server)
    return flask.jsonify(servers=ret)


@app.route("/ajax/settings", methods=["POST"])
@login_required
def ajax__route_settings_post():
    api__trainer.set__settings(request.json)
    return ""


@app.route("/ajax/application/<name>", methods=["GET"])
@login_required
def ajax__route_application(name):
    return flask.jsonify(api__trainer.get__configuration__applications_app(name))


@app.route("/ajax/application/<name>/configuration", methods=["GET"])
@login_required
def ajax__route_application_configuration(name):
    return flask.jsonify(api__trainer.get__configuration__applications_app__config(name))


@app.route("/ajax/server/<name>/logs", methods=["GET"])
@login_required
def ajax__route_server_logs(name):
    return flask.jsonify(logs=api__trainer.get__status__server_logs(
        name, search=flask.request.args.get("search"), limit=flask.request.args.get("limit")))


@app.route("/ajax/server/<name>", methods=["GET"])
@login_required
def ajax__route_server(name):
    return flask.jsonify(server=api__trainer.get__status__server(name))


@app.route("/ajax/server/<name>/audit", methods=["GET"])
@login_required
def ajax__route_server_audit(name):
    return flask.jsonify(api__trainer.get__status__server_audit(name))


@app.route("/ajax/application/<name>", methods=["POST"])
@login_required
def ajax__route_application_post(name):
    api__trainer.set__configuration__applications_app(name, request.json)
    return ""


@app.route("/ajax/application/<name>/configuration", methods=["POST"])
@login_required
def ajax__route_application_post_configuration(name):
    api__trainer.set__configuration__applications_app__config(name, request.json)
    return ""


@app.route("/settings", methods=["POST"])
@login_required
def route_settings_save():
    return redirect("/settings")


@app.route("/application/<name>/scaling", methods=["GET"])
@login_required
def route_application_scaling(name):
    return render_template("application_settings.html", name=name)


@app.route("/application/<name>/configuration", methods=["GET"])
@login_required
def route_application_configuration(name):
    return render_template("application_configuration.html", name=name)


@app.route("/application/<name>/events", methods=["GET"])
@login_required
def route_application_events(name):
    return render_template("application_events.html", name=name)


@app.route("/application/<name>/logs", methods=["GET"])
@login_required
def route_application_logs(name):
    return render_template("application_logs.html", name=name)


@app.route("/ajax/events", methods=["GET"])
@login_required
def route_events():
    return flask.jsonify(
        events=api__trainer.get__audit(search=flask.request.args.get("search"), limit=flask.request.args.get("limit")))


@app.route("/application/<name>/server/<serverid>", methods=["GET"])
@login_required
def route_application_server(name, serverid):
    return render_template("application_server.html", name=name, serverid=serverid)


@app.route("/application/<name>/overview", methods=["GET"])
@login_required
def route_application_overview(name):
    return render_template("application_overview.html", name=name)


@app.route("/ajax/application/<name>/servers", methods=["GET"])
@login_required
def ajax__route_application_servers(name):
    servers = []
    cloud_layout = api__trainer.get__configuration__cloud_state()
    for hostid, server in cloud_layout["Current"]["Layout"].items():
        for name, application in server["Apps"].items():
            if name == name:
                servers.append(server)
    return flask.jsonify(servers=servers)


@app.route("/ajax/application/<name>/servers/desired", methods=["GET"])
@login_required
def ajax__route_application_servers_desired(name):
    servers = []
    cloud_layout = api__trainer.get__configuration__cloud_state()
    for hostid, server in cloud_layout["Desired"]["Layout"].items():
        for name, application in server["Apps"].items():
            if name == name:
                servers.append(server)
    return flask.jsonify(servers=servers)


@app.route("/ajax/application/<name>/servers/memory", methods=["GET"])
@login_required
def ajax__route_application_servers_memory(name):
    return flask.jsonify(memory=api__trainer.get__status__application_statistics(name))


@app.route("/ajax/application/<name>/count", methods=["GET"])
@login_required
def ajax__route_application_count(name):
    return flask.jsonify(count=api__trainer.get__status__application_count(name))


@app.route("/ajax/application/<name>/events", methods=["GET"])
@login_required
def ajax__route_application_events(name):
    return flask.jsonify(
        events=api__trainer.get__status__application_events(name, search=flask.request.args.get("search"),
                                                            limit=flask.request.args.get("limit")))


@app.route("/ajax/server/<name>/events", methods=["GET"])
@login_required
def ajax__route_server_events(name):
    return flask.jsonify(events=api__trainer.get__status__server_audit(name, search=flask.request.args.get("search"),
                                                                       limit=flask.request.args.get("limit")))


@app.route("/ajax/server/<name>/memory", methods=["GET"])
@login_required
def ajax__route_server_memory(name):
    return flask.jsonify(memory=api__trainer.get__status__server_memory(name))


@app.route("/ajax/application/<application>/servers/<server>/memory", methods=["GET"])
@login_required
def ajax__route_application_server_memory(application, server):
    return flask.jsonify(memory=api__trainer.get__status__application_server_memory(server, application))


@app.route("/ajax/application/<name>/logs", methods=["GET"])
@login_required
def ajax__route_application_logs(name):
    return flask.jsonify(logs=api__trainer.get__status__application_logs(name, search=flask.request.args.get("search"),
                                                                         limit=flask.request.args.get("limit")))


def extract_command(string_command):
    p = re.compile('([a-z]+)\s(.*)')
    m = p.match(string_command)
    return m.group(1).strip(), m.group(2).strip()


@app.route("/application", methods=["POST"])
@login_required
def route_application__add():
    application = request.json
    api__trainer.set__configuration__applications_app(application["Name"], application)
    return ""


@app.route("/server/<name>/overview")
@login_required
def route_server(name):
    return render_template("server_overview.html", name=name)


@app.route("/server/<name>/logs")
@login_required
def route_server_logs(name):
    return render_template("server_logs.html", name=name)


@app.route("/server/<name>/events")
@login_required
def route_server_events(name):
    return render_template("server_events.html", name=name)


@app.route("/application/<name>", methods=["POST"])
@login_required
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
@login_required
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


@app.route("/properties")
@login_required
def route_properties():
    return render_template("properties.html")


@app.route("/properties/<name>")
@login_required
def route_properties_name(name):
    return render_template("properties_edit.html", name=name)


@app.route("/ajax/properties", methods=["POST"])
@login_required
def ajax__route_properties_post():
    api__trainer.set__properties(request.json)
    return ""


@app.route("/ajax/properties/<name>", methods=["POST"])
@login_required
def ajax__route_properties_post_name(name):
    api__trainer.set__properties(request.json)
    return ""

@app.route("/ajax/properties/<name>", methods=["GET"])
@login_required
def ajax__route_properties_get_post(name):
    return flask.jsonify(properties=api__trainer.get__properties_by_name(name))


@app.route("/ajax/properties", methods=["GET"])
@login_required
def ajax__route_properties_get():
    return flask.jsonify(properties=api__trainer.get__properties())
