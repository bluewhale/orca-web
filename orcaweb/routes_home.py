import re
import uuid

import flask
from flask import render_template
from flask import request

from orcaweb import app
from orcaweb.services import api__trainer


@app.route("/")
def route_dashboard():
    return render_template("dashboard.html", configuration=api__trainer.get__configuration__applications())


@app.route("/application/<name>", methods=["GET"])
def route_application(name):
    return render_template("application.html", application=api__trainer.get__configuration__applications_app(name))


def extract_command(string_command):
    p = re.compile('([a-z]+)\s(.*)')
    m = p.match(string_command)
    return m.group(1).strip(), m.group(2).strip()


@app.route("/application", methods=["POST"])
def route_application__add():
    app = {
        "Name": request.form.get("name")
    }
    api__trainer.set__configuration__applications_app(app)
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

    existing_configuration["LoadBalancer"] = request.form.get("LoadBalancer")
    existing_configuration["Network"] = request.form.get("Network")

    api__trainer.set__configuration__applications_app(existing_configuration)
    return flask.redirect("/application/" + name)


