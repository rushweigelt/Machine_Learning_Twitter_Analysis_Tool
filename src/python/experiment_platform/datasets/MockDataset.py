from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

from .BaseDataset import BaseDataset

class MockDataset(BaseDataset):
    def __init__(self):
        self.name = "Mock Dataset"
        self.X, self.y = load_breast_cancer(return_X_y=True)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, random_state=0)