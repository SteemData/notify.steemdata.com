FROM python:3.6.1

COPY . /app
WORKDIR /app

ENV PRODUCTION yes
ENV FLASK_HOST 0.0.0.0

RUN cd /app && \
    apt-get update && \
    pip install -r requirements.txt
