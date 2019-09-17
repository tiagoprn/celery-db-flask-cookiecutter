.PHONY: help
SHELL := /bin/bash

help:  ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

clean:  ## Clean python bytecodes, cache...
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@find . -name ".cache" -type d | xargs rm -rf
	@find . -name ".coverage" -type f | xargs rm -rf

init-env:
	@cp etc/.env.sample .env
	@echo '.env file initialized at the project root. Customize it as you may.'

requirements:  ## Install pip requirements
	@pip install --upgrade pip
	@pip install -r requirements-dev.txt

runserver-dev:  ## Run flask development server
	set -a && source .env && set +a && flask run

runserver:  ## Run gunicorn production server
	 set -a && source .env && set +a && gunicorn -c worker_settings.py {{ cookiecutter.project_slug }}:app -b 127.0.0.1:5000 --log-level INFO

shell:  ## initialize a shell
	 set -a && source .env && set +a && flask shell

routes:  ## show all configured api routes
	 set -a && source .env && set +a && flask routes

api-test:  ## make a request with curl to check the app is responding
	curl -i http://localhost:5000/api/echo/hey

