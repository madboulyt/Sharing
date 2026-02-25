#! /usr/bin/env bash

# Exit immediately if a command exits with a non-zero status.
set -e

if [ "$#" -lt 2 ] \
        || ! ([ "$1" == "local" ] \
        || [ "$1" == "remote" ]) \
        || ! ([ "$2" == "lock" ] \
        || [ "$2" == "testing" ] \
        || [ "$2" == "publish-app" ] \
        || [ "$2" == "publish-image" ] \
        || [ "$2" == "dev" ] \
        || [ "$2" == "run" ] \
        || [ "$2" == "up" ] \
        || [ "$2" == "exec" ] \
        || [ "$2" == "stop" ] \
        || [ "$2" == "ptw" ] \
        || [ "$2" == "jupyter" ] \
        || [ "$2" == "build-image" ] \
        || [ "$2" == "pytest" ]) ; then
    echo "Usage: $0 [local|remote]" \
        "[lock|publish-app|publish-image|dev|run|up|exec|stop|ptw|jupyter|build-image|pytest]"
    exit 1
fi

source .env

if [ "$1" == "local" ] ; then
    echo "Check Okta MFA ..."
    source ./scripts/local_login.sh
    $(aws configure export-credentials --profile $AWS_PROFILE --format env)
    build () {
        docker build -t $APP_NAME \
            --build-arg POETRY_HTTP_BASIC_MOZN_USERNAME=$POETRY_HTTP_BASIC_MOZN_USERNAME \
            --build-arg POETRY_HTTP_BASIC_MOZN_PASSWORD=$POETRY_HTTP_BASIC_MOZN_PASSWORD \
            --build-arg ECR_REPO=$ECR_REPO \
            --build-arg IMAGE_TAG=$IMAGE_TAG \
            --build-arg APP_PATH=$APP_PATH \
            --build-arg ECR_PYTHON=$ECR_PYTHON \
            --build-arg PYTHON_TAG=$PYTHON_TAG \
            --target "$1" \
            . \
            -f "$2"
    }
fi

if [ "$1" == "remote" ] ; then
    source ./scripts/remote_login.sh
    build () {
        docker build -t $APP_NAME \
            --build-arg POETRY_HTTP_BASIC_MOZN_USERNAME=$POETRY_HTTP_BASIC_MOZN_USERNAME \
            --build-arg POETRY_HTTP_BASIC_MOZN_PASSWORD=$POETRY_HTTP_BASIC_MOZN_PASSWORD \
            --build-arg ECR_REPO=$ECR_REPO \
            --build-arg IMAGE_TAG=$IMAGE_TAG \
            --build-arg APP_PATH=$APP_PATH \
            --build-arg ECR_PYTHON=$ECR_PYTHON \
            --build-arg PYTHON_TAG=$PYTHON_TAG \
            --target "$1" \
            . \
            -f "$2"
    }
fi

if [ "$2" == "publish-app" ] ; then
    build "publish" "dev.Dockerfile"
fi

if [ "$2" == "build-image" ] ; then
    build "development" "dev.Dockerfile"
    docker tag $APP_NAME $ECR_REPO:$IMAGE_TAG
fi

if [ "$2" == "lock" ] ; then
    build "development" "dev.Dockerfile"
    docker run --rm \
        --name=$APP_NAME \
        -v `pwd`:$APP_PATH \
        $APP_NAME \
        "poetry lock -vv"
fi

if [ "$2" == "dev" ] ; then
    build "development" "dev.Dockerfile"
    docker run --rm -it \
        --name=$APP_NAME \
        -v `pwd`:$APP_PATH \
        $APP_NAME \
        "bash"
fi

if [ "$2" == "run" ] ; then
    build "development" "dev.Dockerfile"
    docker run --rm \
        --name=$APP_NAME \
        -v `pwd`:$APP_PATH \
        $APP_NAME \
        "${*:3}"
fi

if [ "$2" == "up" ] ; then
    build "development" "dev.Dockerfile"
    docker run --rm -d \
        --name=$APP_NAME \
        -v `pwd`:$APP_PATH \
        $APP_NAME \
        "sleep infinity"
fi

if [ "$2" == "exec" ] ; then
    docker exec $APP_NAME ${*:3}
fi

if [ "$2" == "stop" ] ; then
    docker stop $APP_NAME
fi

if [ "$2" == "jupyter" ] ;  then
    build "development" "dev.Dockerfile"
    docker run --rm -it \
        --name="${APP_NAME}-jupyter" \
        -v `pwd`:$APP_PATH \
        -p 8881:8888 \
        $APP_NAME \
        "poetry run jupyter-lab --allow-root --autoreload --ip 0.0.0.0"
fi

if [ "$2" == "ptw" ] ; then
    build "development" "dev.Dockerfile"
    docker run --rm -it \
        --name="${APP_NAME}-ptw" \
        -v `pwd`:$APP_PATH \
        $APP_NAME \
        "ptw -- -vv --cov=arabic_cleaning --cov-report=term-missing --color=yes"
fi

if [ "$2" == "pytest" ] ; then
    build "development" "dev.Dockerfile"
    docker run --rm \
        --name=$APP_NAME \
        -v `pwd`:$APP_PATH \
        $APP_NAME \
        "pytest -vv ./tests --cov=arabic_cleaning --cov-report=term-missing --color=yes"
fi
