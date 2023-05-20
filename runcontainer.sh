#!/bin/sh

if [ -n $CONTAINER_TYPE ]
then
    if [ "$CONTAINER_TYPE" = "api" ]
    then
        cd app
        cmd="uvicorn main:app --host 0.0.0.0 --port 8000"
    elif [ "$CONTAINER_TYPE" = "worker" ]
    then
        cmd="celery -A app.worker.tasks worker -E --loglevel=INFO"
    elif [ "$CONTAINER_TYPE" = "flower" ]
    then
        cmd="celery -A app.worker.tasks flower --url_prefix=flower --loglevel=INFO"
    else
        echo "invalid container type"
        exit 1
    fi
else
    echo "container type is not set"
    exit 1
fi

exec $cmd