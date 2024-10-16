#!/bin/sh
REPOSITORY_NAME=tyronextian
IMAGE_NAME=debian_python_base
TAG=3.10.13

docker build -t ${IMAGE_NAME}:${TAG} -f base.Dockerfile .
docker tag ${IMAGE_NAME}:${TAG} ${REPOSITORY_NAME}/${IMAGE_NAME}:${TAG}
#docker push ${IMAGE_NAME}:${TAG}

echo "docker pull ${REPOSITORY_NAME}/${IMAGE_NAME}:${TAG}"