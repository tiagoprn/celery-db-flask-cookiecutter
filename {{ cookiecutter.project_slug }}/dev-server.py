from {{ cookiecutter.project_slug }} import factory

if __name__ == "__main__":
    app = factory.create_app()
    app.run(host='0.0.0.0')
