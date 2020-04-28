import logging
import os
from datetime import datetime
from functools import lru_cache
from pathlib import Path

import flask
from flask import Blueprint, jsonify

from {{ cookiecutter.project_slug }}.exceptions import APIError

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


@blueprint.route('/api/echo/<value>', methods=['GET'])
def echo(value):
    return jsonify({'value': value})


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
