#!/bin/bash

# For this script to run successfully, it is intended to run from the Makefile,
# and not be called directly from here.
DOCKER_REGISTRY_URL=hub.docker.com

echo "current-dir=$PWD"

APP_NAME=$1
IMAGE_NAME_PREFIX=tiagoprn
APP_NAME=$IMAGE_NAME_PREFIX/$APP_NAME
DOCKERFILE_NAME=Dockerfile
APP_VERSION=$(cat $PWD/VERSION)
UID=$(id -u)
GID=$(id -g)

echo "Building image for APP_NAME=$APP_NAME, DOCKERFILE_NAME=$DOCKERFILE_NAME, UID=$UID, GID=$GID..." \
    && docker build -t $APP_NAME --pull --no-cache --build-arg UID=$UID --build-arg GID=$GID  -f $DOCKERFILE_NAME . \
    && echo "Successfully built image for APP_NAME=$APP_NAME, DOCKERFILE_NAME=$DOCKERFILE_NAME, UID=$UID, GID=$GID."

# To build on CircleCI / GitLab:
# https://github.com/docker-slim/docker-slim#running-containerized
echo "Building slim image for APP_NAME=$APP_NAME, DOCKERFILE_NAME=$DOCKERFILE_NAME, UID=$UID, GID=$GID..." \
    && docker run -it --rm -v /var/run/docker.sock:/var/run/docker.sock dslim/docker-slim build $APP_NAME \
    && echo "Successfully built slim image for APP_NAME=$APP_NAME, DOCKERFILE_NAME=$DOCKERFILE_NAME, UID=$UID, GID=$GID."

echo "Tagging APP_NAME=${APP_NAME} as ${APP_VERSION}..." \
    && docker tag $APP_NAME $APP_NAME:$APP_VERSION \
    && echo "APP_NAME=${APP_NAME} successfully tagged as ${APP_VERSION}."

echo "Tagging slim APP_NAME=${APP_NAME}.slim as ${APP_VERSION}..." \
    && docker tag $APP_NAME.slim $APP_NAME.slim:$APP_VERSION \
    && echo "APP_NAME=${APP_NAME}.slim successfully tagged as ${APP_VERSION}."

for arg in "$@"
do
    if [ "$arg" == "--remote" ]; then
        echo '# TODO: change below to push and tag into a remote docker registry.'
        # echo "Pushing docker IMAGE_ID=${IMAGE_ID} into the docker registry..."
        # echo "Tagging IMAGE_ID=${IMAGE_ID}, DOCKER_REGISTRY_URL=${DOCKER_REGISTRY_URL}, APP_NAME=${APP_NAME}, APP_VERSION=${APP_VERSION} to prepare to the docker registry..." \
            # && docker tag $IMAGE_ID "${DOCKER_REGISTRY_URL}/${APP_NAME}:${APP_VERSION}" \
            # && docker tag $IMAGE_ID "${DOCKER_REGISTRY_URL}/${APP_NAME}:latest" \
            # && echo "IMAGE_ID=${IMAGE_ID} sucessfully tagged! o/"
        # echo "Uploading IMAGE_ID=${IMAGE_ID} to our docker registry..." \
            # && docker push "${DOCKER_REGISTRY_URL}/${APP_NAME}:latest" \
            # && docker push "${DOCKER_REGISTRY_URL}/${APP_NAME}:${APP_VERSION}" \
            # && echo "IMAGE_ID=${IMAGE_ID} upload successfully finished! o/"
    fi
done
