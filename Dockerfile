FROM python:3.9

RUN pip install pipenv

ENV PRJ_DIR /usr/

WORKDIR ${PRJ_DIR}/app

COPY Pipfile Pipfile.lock ${PRJ_DIR}

RUN pipenv install --system --deploy

EXPOSE 8000

COPY ./app ${PRJ_DIR}/app
