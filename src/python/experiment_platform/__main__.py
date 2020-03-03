import mlflow
from time import time
import random
import numpy as np

from datasets import all_datasets
from models import all_models
from converters import all_converters


preprocessing_cache = {}

while True:
    dataset = random.choice(all_datasets)
    if dataset in preprocessing_cache:
        X, y = preprocessing_cache[dataset]
    else:
        print(f"loading dataset {dataset.name}")
        dataset.load()
        X, y = dataset.X, dataset.y
        for converter in all_converters:
            X, y = converter(X, y)
        preprocessing_cache[dataset] = (X, y)

    mlflow.set_experiment(dataset.name)
    print(f"Starting experiment for {dataset.name}")

    model = random.choice(all_models)
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
