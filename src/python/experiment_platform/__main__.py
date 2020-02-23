import mlflow
from time import time

from datasets import all_datasets
from models import custom_models
from converters import all_converters


def run_all_models():
    run_models(custom_models)


def run_models(models):
    for dataset in all_datasets:
        dataset.load()
        X, y = dataset.X, dataset.y
        for converter in all_converters:
            X, y = converter(X, y)
        print(f"Starting experiment for {dataset.name}")
        print("-"*30)
        mlflow.set_experiment(dataset.name)
        for model in models:
            print(f"Starting run with {model.name}")
            with mlflow.start_run(run_name=f"{model.name} {time()}"):
                mlflow.set_tag("model", model.name)
                params = model.get_params()
                if "estimator" in params: #This parameter won't save nicely, so just remove it
                    del params["estimator"]
                mlflow.log_params(params)
                metrics = model.scores(X, y, scoring=['recall', 'accuracy'])
                mlflow.log_metrics(metrics)
                model.save(
                    artifact_path=model.name,
                )


run_all_models()
