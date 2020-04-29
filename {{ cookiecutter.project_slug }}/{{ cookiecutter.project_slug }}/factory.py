import os

from celery import Celery

from flask import Flask
from {{cookiecutter.project_slug}}.celery_utils import init_celery

PKG_NAME = os.path.dirname(os.path.realpath(__file__)).split("/")[-1]


def create_app(app_name=PKG_NAME, **kwargs):
    app = Flask(app_name)
    if kwargs.get("celery"):
        init_celery(kwargs.get("celery"), app)
    from {{ cookiecutter.project_slug }}.api import blueprint as api_blueprint

    app.register_blueprint(api_blueprint)
    return app


def make_celery(app_name=__name__):
    # TODO: better read values below from a `settings.py`
    user = 'user'
    password = 'password'
    host = '127.0.0.1'
    port = 5672
    broker = f'amqp://{user}:{password}@{host}:{port}//'
    configuration = {
        'task_default_queue': '{{ cookiecutter.project_slug }}-default',
        'task_create_missing_queues': True,
    }
    return Celery(app_name, broker=broker, config_source=configuration)
