"""
This module is used to create extensions, according to the recommendation
from the official flask docs for app factories:
https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/#factories-extensions
"""

from celery import Celery
from flasgger import Swagger
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from {{cookiecutter.project_slug}} import settings


bcrypt = Bcrypt()
jwt = JWTManager()


def init_swagger(app):
    return Swagger(app, template=settings.SWAGGER_TEMPLATE)


def init_bcrypt(app):
    app.config['JWT_SECRET_KEY'] = settings.JWT_SECRET_KEY
    bcrypt.init_app(app)


def init_jwt(app):
    app.config['JWT_SECRET_KEY'] = settings.JWT_SECRET_KEY
    jwt.init_app(app)


def init_celery(app):
    # Build the broker URL from settings
    user = settings.QUEUE_USER
    password = settings.QUEUE_PASSWORD
    host = settings.QUEUE_HOST
    port = settings.QUEUE_PORT
    broker = f'amqp://{user}:{password}@{host}:{port}//'

    # Create the Celery instance with the Flask app's import name
    celery = Celery(app.import_name)

    # Set the broker and other Celery configuration values
    celery.conf.broker_url = broker
    configuration = {
        'task_default_queue': settings.DEFAULT_QUEUE_NAME,
        'task_create_missing_queues': True,
        'task_routes': settings.TASKS_QUEUES,
        'accept_content': ['pickle', 'json'],
    }

    if settings.IS_DEV_APP:
        configuration['task_always_eager'] = True

    celery.conf.update(configuration)

    # If you want to merge in additional configuration from the Flask app
    # without overwriting the broker_url, do so here:
    flask_config = app.config.copy()
    flask_config.pop('broker_url', None)
    celery.conf.update(flask_config)

    # Wrap tasks to run within the Flask app context
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    # Optionally store the celery instance on the app for later use
    app.extensions = getattr(app, 'extensions', {})
    app.extensions['celery'] = celery

    return celery


db = SQLAlchemy()
migrate = Migrate()


# pylint: disable=unused-import
def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # models must be imported here so that the migrations app detect them
    from {{ cookiecutter.project_slug }}.models import User

    migrate.init_app(app, db)
