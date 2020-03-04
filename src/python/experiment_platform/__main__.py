"""
Entrypoint for the experiment platform. Running this module will randomly and
continually train new models on available datasets. All training results and
model artifacts are stored in a central MLFlow server, specified with the
MLFLOW_TRACKING_URI environment variable.
"""
import random
from time import time
import mlflow
import numpy as np

from .datasets import ALL_DATASETS
from .models import ALL_MODELS
from .data_processing import process_all


preprocessing_cache = {}

while True:
    dataset = random.choice(ALL_DATASETS)
    if dataset in preprocessing_cache:
        X, y = preprocessing_cache[dataset]
    else:
        print(f"loading dataset {dataset.name}")
        dataset.load()
        X, y = process_all(dataset.X, dataset.y)
        preprocessing_cache[dataset] = (X, y)

    mlflow.set_experiment(dataset.name)
    print(f"Starting experiment for {dataset.name}")

    model = random.choice(ALL_MODELS)
    print(f"Running model {model.name}")

    seed = int(random.random() * 100000)
    np.random.seed(seed)
    print(f"Using random seed {seed}")
    with mlflow.start_run(run_name=f"{model.name} {time()}"):
        mlflow.set_tag("model", model.name)
        params = model.get_params()
        if "estimator" in params:  # This parameter won't save nicely, so just remove it
            del params["estimator"]
        mlflow.log_params(params)
        metrics = model.scores(X, y, scoring=["recall", "accuracy"], cv=dataset.cv)
        mlflow.log_metrics(metrics)
        model.save(artifact_path=model.name,)

# TODO: refactor above logic into train_model(model, dataset) in init
# TODO: create CLI for running specific (model, dataset) pairs
