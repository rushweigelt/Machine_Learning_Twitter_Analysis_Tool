from experiment_platform.datasets import MockDataset
from experiment_platform.models import model_types, custom_models

def run_all_models():
    all_models = custom_models + [m() for m in model_types]
    dataset = MockDataset()
    for model in all_models:
        model.run(dataset)

run_all_models()