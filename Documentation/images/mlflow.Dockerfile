FROM python:3.8
EXPOSE 5000

RUN pip install mlflow==1.6.0
RUN mkdir /mlflow

CMD mlflow server --backend-store-uri /mlflow --default-artifact-root /data/mlflow --host 0.0.0.0