import os

from flask import Flask
from {{cookiecutter.project_slug}}.extensions import (
    celery,
    init_celery,
    init_db,
)

PKG_NAME = os.path.dirname(os.path.realpath(__file__)).split("/")[-1]


def create_app():
    app = Flask(PKG_NAME)

    init_db(app)

    init_celery(celery, app)

    from {{ cookiecutter.project_slug }}.api import blueprint as api_blueprint

    app.register_blueprint(api_blueprint)
    return app
