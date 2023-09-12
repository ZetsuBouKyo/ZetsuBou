FROM python:3.8.16-slim-buster
LABEL maintainer="ZetsuBouKyo"

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PIPENV_VENV_IN_PROJECT=1

WORKDIR /workspace

RUN apt-get update -y
RUN apt-get install ffmpeg libsm6 libxext6 wget git -y

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz

RUN python3 -m pip install --no-cache-dir --upgrade pip
RUN python3 -m pip install --no-cache-dir poetry

COPY . .

RUN python3 -m pip install --no-cache-dir -r requirements.txt

RUN python3 cli.py build statics download

RUN mkdocs build
