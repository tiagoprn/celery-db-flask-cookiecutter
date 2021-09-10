#!/bin/bash

set -eou pipefail

# For this script to run successfully, it is intended to run from the Makefile,
# and not be called directly from here.

echo "current-dir=$PWD"

APP_NAME=$1
IMAGE_NAME_PREFIX=tiagoprn
APP_NAME=$IMAGE_NAME_PREFIX/$APP_NAME
DOCKERFILE_NAME=Dockerfile
APP_VERSION=$(cat "$PWD"/VERSION)
CONTAINER_USER_ID=$(id -u)
CONTAINER_GROUP_ID=$(id -g)

echo "Building image for APP_NAME=$APP_NAME, DOCKERFILE_NAME=$DOCKERFILE_NAME, CONTAINER_USER_ID=$CONTAINER_USER_ID, CONTAINER_GROUP_ID=$CONTAINER_GROUP_ID..."

podman build -t "$APP_NAME" --pull --no-cache --build-arg CONTAINER_USER_ID="$CONTAINER_USER_ID" --build-arg CONTAINER_GROUP_ID="$CONTAINER_GROUP_ID" -f "$DOCKERFILE_NAME" .

echo "Successfully built image for APP_NAME=$APP_NAME, DOCKERFILE_NAME=$DOCKERFILE_NAME, CONTAINER_USER_ID=$CONTAINER_USER_ID, CONTAINER_GROUP_ID=$CONTAINER_GROUP_ID."

echo "Tagging APP_NAME=${APP_NAME} as ${APP_VERSION}..."

podman tag "$APP_NAME" "$APP_NAME":"$APP_VERSION"

echo "APP_NAME=${APP_NAME} successfully tagged as ${APP_VERSION}."

