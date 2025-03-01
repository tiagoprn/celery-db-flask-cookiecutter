.PHONY: help
SHELL := /bin/bash
PROJECT_NAME = {{ cookiecutter.project_slug }}
SHARED_FOLDER=/tmp/shared-docker-$(shell date +%Y%m%d_%H%M%S)
PYTHON_VERSION=3.13

help:  ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

clean:  ## Clean python bytecodes, optimized files, logs, cache, coverage...
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@rm -f .coverage
	@rm -rf htmlcov/
	@rm -fr .pytest_cache/
	@rm -f coverage.xml
	@rm -f *.log
	@find . -name "celerybeat-schedule*" | xargs rm -rf

init-env:  ## create a .env file with the environment variables.
	@cp etc/env.sample .env
	@echo '.env file initialized at the project root. Customize it as you may.'
	@echo '0.1' > VERSION
	@echo 'Created file containing the app version.'

dev-setup-uv:  ## setup the development environment using uv
	@read -p "Make sure you have the uv python package manager installed. Press Enter to continue..." dummy
	@echo 'Updating uv...'
	@uv self update
	@echo "Installing python $$PYTHON_VERSION on uv..."
	@uv python install $(PYTHON_VERSION)
	@echo "Creating a python venv on the project folder..."
	@uv venv --python $(PYTHON_VERSION)
	@echo "Python venv created using uv under '.venv' on the project root."
	@echo "Activate the venv now to install the project requirements."

dev-setup-ruff:  ## install ruff globally (using uv)
	@echo 'This will install ruff (linter and formatter) globally.'
	@uv tool install ruff@latest

requirements:  ## Install pip requirements using uv
	@read -p "This uses the uv python package manager. It will override your requirements.txt from requirements.in." dummy
	@read -p "Make sure you have manually activated the virtualenv with the 'source' command before continuing!" dummy
	@uv pip compile requirements.in --output-file requirements.txt
	@uv pip install -r requirements.txt

runserver: migrate  ## Run gunicorn production server
	 # Gunicorn needs to bind to 0.0.0.0 so to be able to receive requests from the docker network,
	 # otherwise it will only receive them locally. With '-' logs are redirected to stdout (because containers)
	 # /dev/shm tells to the workers to use shared memory, and in-memory filesystem, instead of
	 # using files, which are slower and can degrade performance - and are not a good practice for
	 # containers anyhow, since they must redirect all of theirs logs to stdout/stderr.
	 set -a && source .env && set +a && gunicorn --worker-tmp-dir /dev/shm -c gunicorn_settings.py $(PROJECT_NAME):app -b 0.0.0.0:5000 --log-level INFO  --access-logfile '-' --error-logfile '-'

runworker: clean migrate  ## Run a production celery worker
	@python celery_worker.py worker --loglevel=INFO --autoscale=50,5 --without-heartbeat --without-gossip --without-mingle --queues=$(PROJECT_NAME)-default,$(PROJECT_NAME)-high-priority

migrations: clean  ## create/upgrade migrations
	@set -a && source .env && set +a && flask db init || /bin/true && flask db migrate

migrate: clean  ## upgrade database to the most recent migration
	@set -a && source .env || /bin/true && set +a && flask db upgrade

shell:  ## initialize a shell
	 set -a && source .env && set +a && flask shell

style-autofix:	## Run ruff to format your code
	@echo 'running ruff...'
	@ruff format

style:  ## Run ruff to check code style
	@echo 'running ruff format check...'
	@ruff format --check

docker-build-local-app: clean  ## Build local docker image (app)
	@./scripts/build-docker-image.sh $(PROJECT_NAME)

docker-run-local-app-container: clean  ## Run the app docker image locally
	echo "You can exchange files with the container on the directory $(SHARED_FOLDER) on the host and /shared on the container."
	@mkdir -p $(SHARED_FOLDER)
	$(eval IMAGE_NAME=$(shell bash -c "docker images| grep $(PROJECT_NAME)| grep `cat VERSION` | grep -v slim | cut -d ' ' -f 1"))
	@echo "IMAGE_NAME=$(IMAGE_NAME)"
	@echo '---'
	@echo 'Below is the CONTAINER_ID:'
	@docker run --rm -d -p 5000:5000 --name $(PROJECT_NAME) --env-file .env --network bridge --mount type=bind,source=$(SHARED_FOLDER),target=/shared ${IMAGE_NAME}

podman-build-local-app: clean  ## Build local podman image (app)
	@./scripts/build-podman-image.sh $(PROJECT_NAME)

podman-run-local-app-container: clean  ## Run the app podman image locally
	echo "You can exchange files with the container on the directory $(SHARED_FOLDER) on the host and /shared on the container."
	@mkdir -p $(SHARED_FOLDER)
	$(eval IMAGE_NAME=$(shell bash -c "podman images| grep $(PROJECT_NAME)| grep `cat VERSION` | grep -v slim | cut -d ' ' -f 1"))
	@echo "IMAGE_NAME=$(IMAGE_NAME)"
	@echo '---'
	@echo 'Below is the CONTAINER_ID:'
	@podman run --rm -d -p 5000:5000 --name $(PROJECT_NAME) --network bridge ${IMAGE_NAME}

lint:  ## Run the ruff linter to enforce our coding practices
	@printf '\n --- \n >>> Running linter...<<<\n'
	@ruff check
	@printf '\n FINISHED! \n --- \n'

lint-autofix:  ## Run the ruff linter to enforce our coding practices, and autofix errors that are fixable
	@printf '\n --- \n >>> Running linter...<<<\n'
	@ruff check --fix
	@printf '\n FINISHED! \n --- \n'

test: clean migrate  ## Run the test suite
	@cd $(PROJECT_NAME) && py.test -s -vvv

coverage: clean migrate  ## Run the test coverage report
	@py.test --cov-config .coveragerc --cov $(PROJECT_NAME) $(PROJECT_NAME) --cov-report term-missing

local-healthcheck-readiness:  ## Run curl to make sure the app/worker is ready
	@curl http://localhost:5000/health-check/readiness

local-healthcheck-liveness:  ## Run curl to make sure the app/worker is live
	@curl http://localhost:5000/health-check/liveness

dev-infra-start: clean  ## Start docker infrastructure containers for development (postgresql, rabbitmq)
	@docker compose up -d

dev-infra-stop: clean  ## Stop docker infrastructure containers
	@docker compose stop

dev-infra-delete: docker-compose-stop  ## Delete docker infrastructure containers
	@docker compose rm -f

dev-api-docs:  ## Print URL of the API docs
	@echo 'Visit 0.0.0.0/apidocs on your browser to view the swagger API docs.'

dev-routes:  ## show all configured API routes (endpoints)
	@set -a && source .env && set +a && flask routes

dev-api-test:  ## make a request with curl to check the API is responding
	@curl -i -L http://localhost:5000/welcome/you

dev-runserver: migrate  ## Run flask development server
	set -a && source .env && set +a && python dev-server.py

dev-runworker: clean migrate  ## Run a development celery worker
	@python celery_worker.py worker --loglevel=DEBUG --pool=solo --queues=$(PROJECT_NAME)-default,$(PROJECT_NAME)-high-priority
