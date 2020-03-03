from abc import ABC, abstractmethod
from sklearn.model_selection import StratifiedKFold


class BaseDataset(ABC):
    def __init__(self):
        self.X = None
        self.y = None
        self.cv = None
