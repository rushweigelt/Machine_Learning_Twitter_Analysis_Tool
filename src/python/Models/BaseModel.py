"""
Defines a base class for all ML models.
"""

import mlflow

class BaseModel():
    def __init__(self, **kwargs,):
        self.params = kwargs
        pass

    def run(self):
        for dataset in self.get_datasets():
            with mlflow.start_run():
                mlflow.set_experiment(dataset.name)
                mlflow.log_params(self.params)
                
                self.train(dataset.X_train, dataset.y_train)
                metrics = self.score(dataset.X_test, dataset.y_test)
                mlflow.log_metrics(metrics)
                
                self.save()

    def train(self, X, y):
        raise NotImplementedError

    def predict(self, X):
        raise NotImplementedError

    def score(self, X, y):
        raise NotImplementedError

    def save(self):
        raise NotImplementedError

    @staticmethod
    def load(self):
        raise NotImplementedError

    @staticmethod
    def get_datasets(self):
        return []