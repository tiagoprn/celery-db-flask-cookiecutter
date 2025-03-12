import os

from flask import Flask
from {{cookiecutter.project_slug}}.extensions import (
    init_celery,
    init_db,
    init_swagger,
    init_bcrypt,
    init_jwt,
)

PKG_NAME = os.path.dirname(os.path.realpath(__file__)).split("/")[-1]


# pylint: disable=import-outside-toplevel
def create_app():
    app = Flask(PKG_NAME)

    init_swagger(app)

    init_db(app)

    init_celery(app)

    init_bcrypt(app)

    init_jwt(app)

    from {{cookiecutter.project_slug}}.api import api_blueprint

    app.register_blueprint(api_blueprint)
    return app
