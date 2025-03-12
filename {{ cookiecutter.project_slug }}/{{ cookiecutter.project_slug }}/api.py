import logging
from datetime import datetime, timedelta
from random import randint

import flask
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)
from {{cookiecutter.project_slug}}.commons import format_list_of_tasks, paginate_query
from {{cookiecutter.project_slug}}.exceptions import APIError
from {{cookiecutter.project_slug}}.models import User, Task
from {{cookiecutter.project_slug}}.settings import VERSION
from {{cookiecutter.project_slug}}.tasks import compute, generate_random_string

api_blueprint = Blueprint("api", __name__)

logger = logging.getLogger(__name__)


@api_blueprint.errorhandler(APIError)
def handle_api_error(error):
    response = jsonify(error.payload)
    response.status_code = error.status_code
    return response


@api_blueprint.route("/compute", methods=["GET"])
def call_compute_task():
    """
    Put a compute task on the queue.

    Runs the compute function asynchronously,
    through sending a task to celery.

    The function called is actually a celery task, that must have
    a celery worker up listening to the queue so that it can be executed.
    ---
    tags:
      - Celery background task
    responses:
      200:
        description: message was put on the queue.
    """

    random_number = randint(1000, 9999)
    now_timestamp = datetime.now().isoformat()

    compute.apply_async(
        kwargs={"random_number": random_number, "now_timestamp": now_timestamp}
    )

    return jsonify({"message": "Successfully sent to queue."})


@api_blueprint.route("/string", methods=["GET"])
def call_generate_random_string_task():
    """
    Put a generate random string task on the queue.

    Runs the generate random string function asynchronously,
    through sending a task to celery.

    The function called is actually a celery task, that must have
    a celery worker up listening to the queue so that it can be executed.
    ---
    tags:
      - Celery background task
    responses:
      200:
        description: message was put on the queue.
    """

    generate_random_string.apply_async()

    return jsonify({"message": "Successfully sent to queue."})


@api_blueprint.route("/health-check/readiness", methods=["GET"])
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
    tags:
      - Healthcheck
    responses:
      200:
        description: show the app as ready, with its app version and type.
    """
    flask_version = flask.__version__
    app_type = f"flask-framework {flask_version}"
    response_dict = {
        "ready": "OK",
        "app_version": VERSION,
        "app_type": f"{app_type}",
    }

    return jsonify(response_dict)


@api_blueprint.route("/health-check/liveness", methods=["GET"])
def liveness():
    """
    Used by k8s, to know if a Container is live.

    The kubelet uses liveness probes to know when to restart a Container. For
    example, liveness probes could catch a deadlock, where an application is
    running, but unable to make progress. Restarting a Container in such a
    state can help to make the application more available despite bugs. This
    will run ON REGULAR INTERVALS.
    ---
    tags:
      - Healthcheck
    responses:
      200:
        description: show the app as live, with its version
                     and the current timestamp.
    """
    timestamp = datetime.now().isoformat()
    response_dict = {
        "live": "OK",
        "version": VERSION,
        "timestamp": timestamp,
    }
    return jsonify(response_dict)


@api_blueprint.route("/welcome/<person>", methods=["GET"])
def welcome(person: str):
    """
    Returns a welcome message with custom text.
    ---
    tags:
      - Example
    parameters:
      - name: person
        in: path
        type: string
        required: true
    responses:
      200:
        description: the welcome message.
    """
    response_dict = {"message": f"Hello, {person}!"}
    return jsonify(response_dict)


@api_blueprint.route("/login", methods=["POST"])
def login():
    """
    Login
    ---
    tags:
      - JWT Auth
    parameters:
      - name: email
        type: string
        required: true
      - name: password
        type: string
        required: true
    responses:
      200:
        description: JWT temporary access token & JWT long-live refresh token
    """
    data = request.get_json()

    email = data["email"]
    password = data["password"]

    user = User.get_by(email=email)
    is_valid_password = user.check_password(password=password)

    if user and is_valid_password:
        # temporary access token:
        access_token = create_access_token(
            identity=str(user.uuid), expires_delta=timedelta(hours=1)
        )

        # long-live refresh token:
        refresh_token = create_refresh_token(identity=str(user.uuid))

        return (
            jsonify(
                {"access_token": access_token, "refresh_token": refresh_token}
            ),
            200,
        )

    return jsonify({"msg": "Invalid credentials"}), 401


@api_blueprint.route("/token/new", methods=["POST"])
@jwt_required(
    refresh=True
)  # with this param, requires the refresh token (long-live one)
def token_refresh():
    """
    Get a new JWT temporary access token (expires in 1 hour)
    ---
    tags:
      - JWT Auth
    responses:
      200:
        description: JWT temporary access token
    """
    identity = get_jwt_identity()
    new_access_token = create_access_token(
        identity=identity, expires_delta=timedelta(hours=1)
    )
    return jsonify({"access_token": new_access_token}), 200


@api_blueprint.route("/user", methods=["POST"])
def create_user():
    """
    Create a new user
    ---
    tags:
      - Users
    parameters:
      - name: username
        type: string
        required: true
      - name: email
        type: string
        required: true
      - name: password
        type: string
        required: true
    responses:
      201:
        description: created user data.
    """
    data = request.get_json()

    new_user = User().register(**data)

    return jsonify({"uuid": str(new_user.uuid)}), 201


@api_blueprint.route("/user", methods=["GET"])
@jwt_required()  # with no params, requires the access token (temporary one)
def get_user():
    """
    Get user info
    ---
    tags:
      - Users
    responses:
      200:
        description: user info
    """
    user_uuid = get_jwt_identity()

    user = User.get_by(uuid=user_uuid)
    return (
        jsonify(
            {
                "uuid": str(user.uuid),
                "username": user.username,
                "email": user.email,
            }
        ),
        200,
    )


@api_blueprint.route("/user", methods=["PATCH"])
@jwt_required()
def update_user():
    """
    Update user info
    ---
    tags:
      - Users
    parameters:
      - name: email
        type: string
        required: false
      - name: password
        type: string
        required: false
    responses:
      200:
        description: updated user info
    """
    user_uuid = get_jwt_identity()

    data = request.get_json()
    user = User.get_by(uuid=user_uuid)

    email = data.get("email")
    password = data.get("password")
    user.update(email=email, password=password)

    password_value = "SUCCESSFULLY CHANGED" if password else "NOT CHANGED"
    return (
        jsonify(
            {
                "uuid": str(user.uuid),
                "email": user.email,
                "password": password_value,
            }
        ),
        200,
    )
