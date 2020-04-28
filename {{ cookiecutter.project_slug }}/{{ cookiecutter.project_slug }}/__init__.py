import os

from flask import Flask

# Import blueprints once everything is configured
from {{ cookiecutter.project_slug }}.api import blueprint as api_blueprint


def create_app():
    app = Flask(__name__)  # pylint: disable=redefined-outer-name
    app.register_blueprint(api_blueprint)
    return app


app = create_app()
