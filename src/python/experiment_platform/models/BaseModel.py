"""
Defines a base class for all ML models.
"""
from abc import ABC, abstractmethod

import mlflow

class BaseModel(ABC):
    def __init__(self):
        self.params = {}

    def run(self, dataset):
        mlflow.set_experiment(dataset.name)
        with mlflow.start_run():
            self.mlflow_run = mlflow.active_run()
            mlflow.set_tag('model', type(self).__name__)
            mlflow.log_params(self.params)
            
            self.fit(dataset.X_train, dataset.y_train)
            metrics = self.scores(dataset.X_test, dataset.y_test)
            mlflow.log_metrics(metrics)
            self.save(uri='model')

    @abstractmethod
    def fit(self, X, y):
        pass

    @abstractmethod
    def predict(self, X):
        pass

    @abstractmethod
    def score(self, X, y):
        pass

    @abstractmethod
    def scores(self, X, y):
        pass

    @abstractmethod
    def save(self, uri=None):
        pass

    @staticmethod
    @abstractmethod
    def load(self):
        pass
