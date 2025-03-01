from {{ cookiecutter.project_slug }}.factory import create_app

app = create_app()
celery = app.extensions['celery']
celery.autodiscover_tasks(['{{ cookiecutter.project_slug }}'])

if __name__ == '__main__':
    import sys  # noqa
    # Remove the script name when running as a script so that the first argument becomes the actual command
    sys.argv = sys.argv[1:]
    celery.start()
