import logging
import os
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from random import randint

import flask
from flask import Blueprint, jsonify
from {{cookiecutter.project_slug}}.exceptions import APIError
from {{cookiecutter.project_slug}}.settings import VERSION
from {{cookiecutter.project_slug}}.tasks import compute, generate_random_string

blueprint = Blueprint('api', __name__)

logger = logging.getLogger(__name__)


@blueprint.errorhandler(APIError)
def handle_api_error(error):
    response = jsonify(error.payload)
    response.status_code = error.status_code
    return response


@blueprint.route('/compute', methods=['GET'])
def call_compute_task():
    """
    Put a compute task on the queue.

    Runs the compute function asynchronously,
    through sending a task to celery.

    The function called is actually a celery task, that must have
    a celery worker up listening to the queue so that it can be executed.
    ---
    responses:
      200:
        description: message was put on the queue.
    """

    random_number = randint(1000, 9999)
    now_timestamp = datetime.now().isoformat()

    compute.apply_async(
        kwargs={'random_number': random_number, 'now_timestamp': now_timestamp}
    )

    return jsonify({'message': 'Successfully sent to queue.'})

@blueprint.route('/string', methods=['GET'])
def call_generate_random_string_task():
    """
    Put a generate random string task on the queue.

    Runs the generate random string function asynchronously,
    through sending a task to celery.

    The function called is actually a celery task, that must have
    a celery worker up listening to the queue so that it can be executed.
    ---
    responses:
      200:
        description: message was put on the queue.
    """

    generate_random_string.apply_async()

    return jsonify({'message': 'Successfully sent to queue.'})

@blueprint.route('/health-check/readiness', methods=['GET'])
def readiness():
    """
    Used by k8s, to know when a container is ready.

    The kubelet uses readiness probes to know when a container
    is ready to start accepting traffic.

    A Pod is considered ready when all of its Containers are ready.
    One use of this signal is to control which Pods are used as
    backends for Services.
    When a Pod is not ready, it is removed from Service load balancers.
    This will run ONLY ONCE.
    ---
    responses:
      200:
        description: show the app as ready, with its app version and type.
    """
    flask_version = flask.__version__
    app_type = f'flask-framework {flask_version}'
    response_dict = {
        'ready': 'OK',
        'app_version': VERSION,
        'app_type': f'{app_type}',
    }

    return jsonify(response_dict)


@blueprint.route('/health-check/liveness', methods=['GET'])
def liveness():
    """
    Used by k8s, to know if a Container is live.

    The kubelet uses liveness probes to know when to restart a Container. For
    example, liveness probes could catch a deadlock, where an application is
    running, but unable to make progress. Restarting a Container in such a
    state can help to make the application more available despite bugs. This
    will run ON REGULAR INTERVALS.
    ---
    responses:
      200:
        description: show the app as live, with its version
                     and the current timestamp.
    """
    timestamp = datetime.now().isoformat()
    response_dict = {
        'live': 'OK',
        'version': VERSION,
        'timestamp': timestamp,
    }
    return jsonify(response_dict)


@blueprint.route('/welcome/<person>', methods=['GET'])
def welcome(person: str):
    """
    Returns a welcome message with custom text.
    ---
    parameters:
      - name: person
        in: path
        type: string
        required: true
    responses:
      200:
        description: the welcome message.
    """
    response_dict = {'message': f'Hello, {person}!'}
    return jsonify(response_dict)
