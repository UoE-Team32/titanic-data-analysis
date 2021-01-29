FROM python:3.8.7-buster

RUN apt-get update -y && apt-get upgrade -y

RUN apt-get install

RUN pip install pipenv

ENV PROJECT_DIR /app

WORKDIR ${PROJECT_DIR}/

COPY Pipfile Pipfile.lock ${PROJECT_DIR}/

RUN pipenv lock

RUN pipenv install --dev --system --deploy

