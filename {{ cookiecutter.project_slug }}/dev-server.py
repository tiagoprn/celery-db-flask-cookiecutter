import {{ cookiecutter.project_slug }}
from {{ cookiecutter.project_slug }} import factory

if __name__ == "__main__":
    app = factory.create_app(celery=app.celery)
    app.run()
