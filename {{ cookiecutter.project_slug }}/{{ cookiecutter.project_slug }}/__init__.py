from {{ cookiecutter.project_slug }}.celery_utils import init_celery
from {{ cookiecutter.project_slug }}.factory import create_app, make_celery

celery = make_celery()
app = create_app()
init_celery(celery, app)
