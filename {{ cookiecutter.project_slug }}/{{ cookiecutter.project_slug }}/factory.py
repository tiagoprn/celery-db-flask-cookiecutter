import os

from flask import Flask
from {{cookiecutter.project_slug}}.extensions import (
    init_celery,
    init_db,
    init_swagger
)

PKG_NAME = os.path.dirname(os.path.realpath(__file__)).split("/")[-1]


# pylint: disable=import-outside-toplevel
def create_app():
    app = Flask(PKG_NAME)

    init_swagger(app)

    init_db(app)

    init_celery(app)

    from {{ cookiecutter.project_slug }}.api import blueprint

    app.register_blueprint(blueprint)
    return app
