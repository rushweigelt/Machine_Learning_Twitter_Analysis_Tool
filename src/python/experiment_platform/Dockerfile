FROM python:3.8

RUN pip install pipenv
WORKDIR /mlflow/projects/code
COPY Pipfile.lock /mlflow/projects/code/
RUN pipenv sync
