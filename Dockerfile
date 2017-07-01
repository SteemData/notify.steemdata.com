FROM python:3.6
MAINTAINER nash <nashruddin.amin@gmail.com>

COPY . /app
WORKDIR /app

ENV PRODUCTION yes
ENV FLASK_HOST 0.0.0.0

RUN cd /app && \
    apt-get update && \
    pip install -r requirements.txt
