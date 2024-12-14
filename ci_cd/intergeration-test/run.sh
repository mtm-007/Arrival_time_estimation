#!/usr/bin/env bash


cd "$(dirname "$0")"

LOCAL_TAG=`date +"%Y-%m-%d-%H-%m"`

export LOCAL_IMAGE_NAME="stream-model-duration:${LOCAL_TAG}"
export PREDICTION_STREAM_NAME="ride_predictions"

docker build -t ${LOCAL_IMAGE_NAME} ..

docker-compose up -d

sleep 1

aws --endpoint-url=http://localhost:4566 \
    kinesis create-stream \
    --stream-name ${PREDICTION_STREAM_NAME} \
    --shard-count 1 || echo "Failed to create stream ${PREDICTION_STREAM_NAME}."


python test_docker.py

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker-compose logs
    docker-compose down
    exit ${ERROR_CODE}
fi

python test_kinesis.py

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker-compose logs
    docker-compose down
    exit ${ERROR_CODE}
fi

docker-compose down

