# celery-db-flask-cookiecutter

This project is a flask template that can be used as a base to develop simple APIs on the Flask Framework with swagger documentation integrated, using celery to run asynchronous jobs and sqlalchemy for database persistance.

## Features

- A Makefile to wrap the most common operations and ease project management and , with commands to run the development server, the shell, etc...

- python 3.13

- flask (latest)

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

``` bash
$ mkdir -p ~/cookiecutters
$ cd ~/cookiecutters
$ git clone  https://github.com/tiagoprn/celery-db-flask-cookiecutter
```

- Enter the folder where your want to create your project locally:

``` bash
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

## OPTION 1 - INSTALL LOCALLY USING AN UV VIRTUALENV:

- This requires the installation of python's uv package manager. To install it:

``` bash

$ curl -LsSf https://astral.sh/uv/install.sh | sh

```

- Create a virtualenv to the project. If you want to use the default provided using uv on the Makefile:

``` bash
$ make dev-setup-uv
```

- Install the development requirements (also using uv):

`$ make requirements`

- Run the make command to create the sample configuration file:

``` bash
$ make init-env
```

- Create a local git repository to bootstrap version control:

``` bash
$ git init
$ git add .
$ git commit -m 'Boostrapping project.'
```

- Now, the development infrastructure containers (postgressql, rabbitmq) must be started:

``` bash

$ make dev-infra-start

```

- Generate the sample db migrations and run them:

``` bash
$ make migrations
$ make migrate
```

- Run the formatter and linter:

NOTE: We use "ruff" as a python linter and formatter, due to its' speed.

If you do not have it installed, you can run this command first:

``` bash

$ make dev-setup-ruff

```

This will install ruff globally, but do not worry. It needs to be explicitly called and you can customize its' behavior per project if you need.

``` bash
$ make style && make style-autofix && make style
$ make lint && make lint-autofix && make lint
```

- Run the test suite:

``` bash
$ make test
```

- Start the development server:

`$ make dev-runserver`

... or start the production server (gunicorn):

`$ make runserver`

Then, check the api documentation URL:

`$ make dev-api-docs`

- Start the development worker:

`$ make dev-runworker`

... or start the production worker (gunicorn):

`$ make runworker`

## OPTION 2 - BUILD AND RUN FROM DOCKER/PODMAN

(TODO: this needs to be tested)

``` bash
$ make docker-build-local-app-container && make docker-run-local-app-container

or...

$ make podman-build-local-app-container && make podman-run-local-app-container
```

Then, check the api documentation:

`$ make dev-api-docs`

