FROM python:3.7-slim
WORKDIR /code
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

COPY requirements.txt requirements.txt

## install dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y gcc libpq-dev && \
    apt-get clean \
    apt-get autoremove -y gcc

RUN python3 -m pip install --upgrade pip -r requirements.txt
COPY . .