"""
The experiment platform is a tool for automatically and repeatedly training
machine learning models against various datasets. All model training results
and artifacts are saved to a central MLFlow server.
"""
import os
from time import time

import mlflow

try:
    PARALLELISM = int(os.getenv("PARALLELISM", "4"))
except ValueError:
    print(
        "Value of PARALLELISM env var was unable to be cast to int. Using default value of 4."
    )
    PARALLELISM = 4


def run_experiment(dataset, model):
    """
    Runs a single experiment for the given dataset, model pair.

    Returns the scoring metrics persisted to MLFlow tracking server.
    """
    mlflow.set_experiment(dataset.name)
    with mlflow.start_run(run_name=f"{model.name} {time()}"):
        mlflow.set_tag("model", model.name)
        params = model.get_params()
        if "estimator" in params:  # This parameter won't save nicely, so just remove it
            del params["estimator"]
        mlflow.log_params(params)
        metrics = model.scores(
            dataset.X, dataset.y, scoring=["recall", "accuracy"], cv=dataset.cv
        )
        mlflow.log_metrics(metrics)
        model.save(artifact_path=model.name,)
        return metrics
