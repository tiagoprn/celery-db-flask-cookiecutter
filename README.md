# celery-db-flask-cookiecutter

This project is a flask template that can be used as a base to develop simple APIs on the Flask Framework with swagger documentation integrated, using celery to run asynchronous jobs and sqlalchemy for database persistance.

## Features

- A Makefile to wrap the most common operations and ease project management and , with commands to run the development server, the shell, etc...

- python 3.9

- flask 2.0

- flasgger (swagger wrapper) as documentation for the API, using doctrings on the API endpoints to write the documentation.

- gunicorn configured to run the project in the production environment.

- pylint as the linter, black as the code formatter, isort to fix import order

- pytest tests, with some plugins to ease presentation.

- tests coverage report.

- celery configured

- SQLAlchemy integration

- environment variables for configuration.

- docker/podman image generation (properly tagged)

- docker-compose configured with the app required infrastructure (rabbitmq as celery broker, postgresql as the database)

- Sample endpoints working


## How to use this cookiecutter

- Install cookiecutter on your distribution (e.g. Ubuntu):

`$ sudo apt install cookiecutter`

- If you want to clone this repository locally to run the cookiecutter also locally:

```
$ mkdir -p ~/cookiecutters
$ cd ~/cookiecutters
$ git clone  https://github.com/tiagoprn/celery-db-flask-cookiecutter
```

- Enter the folder where your want to create your project locally:

```
cd ~/projects/
```

- Run the cookiecutter from the local copy:

`$ cookiecutter ~/cookiecutters/celery-db-flask-cookiecutter`

... or directly from github (recommended):

`$ cookiecutter gh:tiagoprn/celery-db-flask-cookiecutter`

It will ask some questions with sane defaults, and then will generate a folder with the value you
indicated for `project_slug`. Congratulations, this is your new minimal flask project! :)

- Enter the project directory:

`$ cd ~/projects/your-project_slug`

## OPTION 1 - BUILD AND RUN FROM DOCKER/PODMAN

```
$ make docker-build-local-app-container && make docker-run-local-app-container

or...

$ make podman-build-local-app-container && make podman-run-local-app-container
```

Then, check the api documentation:

`$ make api-docs`

## OPTION 2 - INSTALL LOCALLY ON A VIRTUALENV AND RUN FROM THERE

- Create a virtualenv to the project. If you're using pyenv:

```
$ pyenv virtualenv 3.9.1 your-project_slug
$ pyenv activate your-project_slug
```

- Install the development requirements:

`$ make requirements`

- Run the make command to create the sample configuration file:

```
$ make init-env
```

- Create a local git repository to bootstrap version control:

```
$ git init
$ git add .
$ git commit -m 'Boostrapping project.'
```

- Generate the sample db migrations and run them:

```
$ make migrations
$ make migrate
```

- Run the formatter, linter and tests:

```
$ make style && make style-check
$ make lint
$ make test
```

- Start the development server:

`$ make runserver-dev`

... or start the production server (gunicorn):

`$ make runserver`

Then, check the api documentation:

`$ make api-docs`

- Start the development worker:

`$ make runworker-dev`

... or start the production worker (gunicorn):

`$ make runworker`
