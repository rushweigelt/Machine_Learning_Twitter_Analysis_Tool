from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, StratifiedKFold

from .BaseDataset import BaseDataset


class MockDataset(BaseDataset):
    def __init__(self):
        self.name = "Mock Dataset"
        self.X, self.y = load_breast_cancer(return_X_y=True)
        self.cv = StratifiedKFold().split(self.X, self.y)
