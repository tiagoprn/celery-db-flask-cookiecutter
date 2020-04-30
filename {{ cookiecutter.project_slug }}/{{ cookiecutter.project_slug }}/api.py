import logging
import os
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from random import randint

import flask
from flask import Blueprint, jsonify
from {{cookiecutter.project_slug}}.exceptions import APIError
from {{cookiecutter.project_slug}}.tasks import compute, generate_random_string

blueprint = Blueprint('api', __name__)

logger = logging.getLogger(__name__)


@lru_cache(maxsize=None)
def get_app_version():
    root_path = str(Path().absolute())
    with open(os.path.join(root_path, 'VERSION'), 'r') as version_file:
        return version_file.read().replace('\n', '')


@blueprint.errorhandler(APIError)
def handle_api_error(error):
    response = jsonify(error.payload)
    response.status_code = error.status_code
    return response


@blueprint.route('/compute', methods=['GET'])
def call_compute_task():
    random_number = randint(1000, 9999)
    now_timestamp = datetime.now().isoformat()

    # The function below is actually a celery task,
    # that must have a celery worker up listening to
    # the queue so that it can be executed.
    compute.apply_async(
        kwargs={'random_number': random_number, 'now_timestamp': now_timestamp}
    )

    return jsonify({'message': 'Successfully sent to queue.'})

@blueprint.route('/string', methods=['GET'])
def call_generate_random_string_task():
    # The function below is actually a celery task,
    # that must have a celery worker up listening to
    # the queue so that it can be executed.
    generate_random_string.apply_async()

    return jsonify({'message': 'Successfully sent to queue.'})

@blueprint.route('/health-check/readiness', methods=['GET'])
def readiness():
    """
    The kubelet uses readiness probes to know when a Container is ready to
    start accepting traffic. A Pod is considered ready when all of its
    Containers are ready. One use of this signal is to control which Pods are
    used as backends for Services. When a Pod is not ready, it is removed from
    Service load balancers. This will run ONLY ONCE.
    """
    flask_version = flask.__version__
    app_type = f'flask-framework {flask_version}'
    response_dict = {
        'ready': 'OK',
        'app_version': get_app_version(),
        'app_type': f'{app_type}',
    }

    return jsonify(response_dict)


@blueprint.route('/health-check/liveness', methods=['GET'])
def liveness():
    """
    The kubelet uses liveness probes to know when to restart a Container. For
    example, liveness probes could catch a deadlock, where an application is
    running, but unable to make progress. Restarting a Container in such a
    state can help to make the application more available despite bugs. This
    will run ON REGULAR INTERVALS.
    """
    timestamp = datetime.now().isoformat()
    response_dict = {
        'live': 'OK',
        'version': get_app_version(),
        'timestamp': timestamp,
    }

    return jsonify(response_dict)
