FROM python:3.10.13-slim-bullseye
MAINTAINER dwzq
ENV TZ=Asia/Shanghai

ARG drepo="mirrors.aliyun.com"
ARG build_packages="apt-utils \
                    vim \
                    curl \
                    bash \
                    sudo \
                    git \
                    procps \
                    acl \
                    wget \
                    tini \
                    openssh-client \
                    unzip"

RUN sed -i "s#deb.debian.org#${drepo}#g;s#security.debian.org#${drepo}#g" /etc/apt/sources.list && \
    apt update && \
    apt upgrade -y && \
    apt -y install --no-install-recommends ${build_packages} && \
    apt install -y libaio1 && \
    apt clean && \
    rm -rf /var/lib/apt/lists/* \
