from {{ cookiecutter.project_slug }}.factory import create_app

app = create_app()

# Ensure tasks are registered
from {{ cookiecutter.project_slug }} import tasks  # noqa
