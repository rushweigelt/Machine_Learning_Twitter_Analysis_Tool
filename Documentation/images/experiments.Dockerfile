FROM python:3.8

RUN pip install pipenv

# Use src/python as build directory
COPY experiment_platform/ /experiment_platform

RUN cd /experiment_platform && pipenv sync

ENV MLFLOW_TRACKING_URI http://localhost:5000

CMD pipenv run python -m experiment_platform
