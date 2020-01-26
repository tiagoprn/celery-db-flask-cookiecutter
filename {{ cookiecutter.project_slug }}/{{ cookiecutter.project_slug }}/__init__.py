import os

from flask import Flask

# Import blueprints once everything is configured
from {{ cookiecutter.project_slug }}.api import blueprint as api_blueprint

app = Flask(__name__)


# Create blueprints for the API
app.register_blueprint(api_blueprint)
