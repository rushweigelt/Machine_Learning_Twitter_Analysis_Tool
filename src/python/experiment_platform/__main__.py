import mlflow
from time import time

from experiment_platform.datasets import CSVDataset
from experiment_platform.models import custom_models


def run_all_models():
    run_models(custom_models)


def run_models(models):
    dataset = CSVDataset(path='/data/data-sets/processed-data/combined/multi_bot_and_genuine_400k_split.csv')
    mlflow.set_experiment(dataset.name)
    for model in models:
        with mlflow.start_run(run_name=f"{model.name} {time()}"):
            mlflow.set_tag("model", model.name)
            params = model.get_params()
            if "estimator" in params:
                del params["estimator"]
            mlflow.log_params(params)
            metrics = model.scores(dataset.X_test, dataset.y_test)
            mlflow.log_metrics(metrics)
            model.save(uri=model.name)


run_all_models()
