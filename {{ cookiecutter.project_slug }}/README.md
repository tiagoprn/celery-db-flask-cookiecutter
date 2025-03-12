# {{ cookiecutter.project_slug }}

This project was bootstrapped from this cookiecutter template of mine: <https://github.com/tiagoprn/celery-db-flask-cookiecutter>.

(you can use [this](https://readme.so/editor) as a reference on how to build an awesome README file.

## Overview

This project provides a RESTful API for ... using Flask.

The API allow users to:

...

## Test coverage

``` bash

# put the results of the coverage report here

```


## Architecture

See [this](ARCHITECTURE.md)


## Technologies

- `Python` 3.13 and `Flask` (3.1) as the web API framework.

- `uv` for packaging (requirements, additional tooling)

- JWT authentication.

- `bcrypt` for password hashing

- CRUD endpoints for ...

- `pytest` for unit tests, with some plugins to ease presentation.

- `Makefile` to wrap the most common operations and ease project management, with commands to run the development server, shell, etc...

- code style and quality: `ruff` as the linter and formatter (customized with `pyproject.toml`)

- environment variables for configuration (`.env` file)

- Provides a `docker-compose.yml` to set up the development environment:
    - configured with the app required infrastructure (postgresql, rabbitmq)
    - `PostgreSQL` as the database , with `SQLAlchemy` as the abstraction layer
    - Background task processing using `Celery` with `RabbitMQ` as the broker (see [ARCHITECTURE.md](ARCHITECTURE.md) for more details).

- API documentation: I integrated `Flasgger` (`Swagger` wrapper), using doctrings on the API endpoints to write the documentation. But due to a bug I could not deeply investigate I cannot use the "Try It Out" functionality: every time we type the values on the fields, they get automatically deleted. This needs to be solved on a future version.


## How to run this project locally (development environment)

- This requires the installation of python's `uv` package manager. To install it:

``` bash

$ curl -LsSf https://astral.sh/uv/install.sh | sh

```

- Create a virtualenv to the project. If you want to use the default provided using uv on the Makefile:

``` bash

$ make dev-setup-uv

```

- Install the development requirements (also using uv):

``` bash

$ make requirements

```


- Run the make command to create the sample configuration file:

``` bash

$ make init-env

```

- Now, the development infrastructure containers (postgressql, rabbitmq) must be started:

``` bash

$ make dev-infra-start

```

- Generate the db migrations and run them:

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

$ make style; make style-autofix && make style
$ make lint; make lint-autofix && make lint

```

- Run the test suite:

``` bash

$ make test

```

- Start the development server:

``` bash

$ make dev-runserver

```


Then, check the api documentation URL:

``` bash

$ make dev-api-docs

```


- Start the development worker:

``` bash

$ make dev-runworker

```


## etc

### pgcli

You can interact with the postgresql database (making queries) using a cli util called 'pgcli'. It provides some features like autocomplete and others.

To install it (uses uv):

``` bash

$ make dev-setup-pgcli

```

To connect to the database (using pgcli):

``` bash

$ make dev-pgcli

```

### run a specific test with pytest

``` bash

$ pytest -s -k 'test_models' -vvv  --disable-warnings

```


## Future enhancements

### Application

- `PATCH /user`: implement current password confirmation and new password confirmation (2nd time to check their must be equal)

- implement user removal

- RBAC implementation (an admin user could create new users, update other users information, etc...)

- Audit trail for changes on user tables

- implement rate limiting

- populate the database with some users - using a `flask shell` script; add command to the Makefile

- `make lint` (ruff) is showing some errors of not used references. When I removed some variables it pointed as not used the tests broke, so this must be investigated in more detail. But that is also proof the linter is doing its job ;)

- Leverage the background workers which are ready to go to create tasks to send a notification using <ntfy.sh> when a new user registers

- pre-commit hook (install `pre-commit` through `uv` and put command on the `Makefile` to do that)

- Use "git-secret": migrate `.env.JWT_SECRET_KEY` to there

- Apply Clean/Hexagonal Architecture

### Infrastructure

- Functionalities provided by bootstrapping from my cookiecutter template but could not be finished on the initial implementation:
    - Customize the `Dockerfile`, so that the project can be built. Keep generating docker/podman images  (properly tagged).
    - Make sure `gunicorn` is properly configured to run the project in the production environment.

- CI pipeline (github actions):
    - ruff lint/format check
    - tests (with coverage report)
