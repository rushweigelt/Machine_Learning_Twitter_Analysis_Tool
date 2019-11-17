from abc import ABC, abstractmethod

class BaseDataset(ABC):
    def __init__(self):
        self.X = None
        self.X_train = None
        self.X_test = None
        self.y = None
        self.y_train = None
        self.y_test = None
