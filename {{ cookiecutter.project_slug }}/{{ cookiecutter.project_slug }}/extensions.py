"""
The db and migrate objects were created here according to the recommendation
from the official flask docs for app factories:
https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/#factories-extensions
"""

from celery import Celery
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from {{cookiecutter.project_slug}} import settings


def init_celery(celery, app):
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask


def make_celery():
    user = settings.QUEUE_USER
    password = settings.QUEUE_PASSWORD
    host = settings.QUEUE_HOST
    port = settings.QUEUE_PORT
    broker = f'amqp://{user}:{password}@{host}:{port}//'
    configuration = {
        'task_default_queue': settings.DEFAULT_QUEUE_NAME,
        'task_create_missing_queues': True,
        'task_routes': settings.TASKS_QUEUES,
        'accept_content': ['pickle', 'json'],
    }
    if settings.IS_DEV_APP:
        # Tasks will be executed locally instead of being sent to the queue.
        # This allows starting a shell to run a task and it stopping at
        # pdb/ipdb breakpoint to ease debugging.
        configuration['task_always_eager'] = True
    return Celery(
            '{{ cookiecutter.project_slug }}.tasks',
            broker=broker,
            config_source=configuration
    )

celery = make_celery()

db = SQLAlchemy()
migrate = Migrate()


def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    # models must be imported here so that the migrations app detect them
    from {{ cookiecutter.project_slug }}.scripts.models import SampleModel  # pylint: disable=import-outside-toplevel,unused-import

    migrate.init_app(app, db)
