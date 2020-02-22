FROM python:3.8

RUN pip install pipenv

# Use src/python as build directory
COPY experiment_platform/ /code

WORKDIR /code
RUN pipenv sync

CMD python __main__.py