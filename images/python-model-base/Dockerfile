FROM python:3.8

RUN pip install pipenv
WORKDIR /tmp/pipenv
COPY Pipfile* ./
RUN pipenv install