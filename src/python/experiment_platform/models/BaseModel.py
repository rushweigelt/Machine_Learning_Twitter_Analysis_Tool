"""
Defines a base class for all ML models.
"""
from abc import ABC, abstractmethod

import mlflow


class BaseModel(ABC):
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
    def scores(self, X, y, scoring=None):
        pass

    @abstractmethod
    def save(self, uri=None):
        pass

    @staticmethod
    @abstractmethod
    def load(self):
        pass
