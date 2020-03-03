import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GroupKFold, StratifiedKFold

from .BaseDataset import BaseDataset

class CSVDataset(BaseDataset):
    def __init__(self, path=None, label='label', name=None, types=None, group_by=None, **kwargs):
        self.name = name if name else str(path).split('/')[-1]
        self.loaded = False
        self.group_by = group_by
        self.load = lambda: self.__load(path, label, types, group_by, **kwargs)
        
    def __load(self, path, label, types, group_by, **kwargs):
        if self.loaded:
            return
        self.loaded = True

        df = pd.read_csv(path, dtype=types, **kwargs)
        self.y = df[label]
        self.X = df.drop(label, axis=1)

        if self.group_by:
            _, self.groups = np.unique(self.X[group_by], return_inverse=True)
            cross_validator = GroupKFold().split(self.X, self.y, self.groups)
        else:
            cross_validator = StratifiedKFold().split(self.X, self.y)
        # Must convert to list to allow re-use (iterator is only good once)
        self.cv = list(cross_validator)
