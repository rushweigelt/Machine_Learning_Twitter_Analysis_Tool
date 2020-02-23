import pandas as pd
from sklearn.model_selection import train_test_split

from .BaseDataset import BaseDataset

class CSVDataset(BaseDataset):
    def __init__(self, path=None,label='label', name=None, types=None, **kwargs):
        self.name = name if name else str(path).split('/')[-1]
        self.load = lambda:self.__load(path, label, types, **kwargs)
        
    def __load(self, path, label, types, **kwargs):
        df = pd.read_csv(path,dtype=types, **kwargs)
        self.y = df[label]
        self.X = df.drop(label, axis=1)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, random_state=0
        )