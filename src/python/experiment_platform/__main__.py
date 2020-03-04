"""
Entrypoint for the experiment platform. Running this module will randomly and
continually train new models on available datasets. All training results and
model artifacts are stored in a central MLFlow server, specified with the
MLFLOW_TRACKING_URI environment variable.
"""
import random
import itertools

import numpy as np

from experiment_platform import run_experiment
from experiment_platform.datasets import ALL_DATASETS
from experiment_platform.models import ALL_MODELS
from experiment_platform.data_processing import process_all


def main():
    """
    Continually run experiments
    """
    datasets = itertools.cycle(ALL_DATASETS)
    models = itertools.cycle(ALL_MODELS)
    for dataset, model in zip(datasets, models):
        print(f"Using dataset {dataset.name}")
        if not dataset.loaded:
            print(f"Loading dataset {dataset.name}")
            dataset.load()
            dataset.X, dataset.y = process_all(dataset.X, dataset.y)

        seed = int(random.random() * 100000)
        np.random.seed(seed)
        print(f"Using random seed {seed}")

        print(f"Running model {model.name}")
        scores = run_experiment(dataset, model)
        print(f"Results: {scores}")


# TODO: create CLI for running specific (model, dataset) pairs

if __name__ == "__main__":
    main()
