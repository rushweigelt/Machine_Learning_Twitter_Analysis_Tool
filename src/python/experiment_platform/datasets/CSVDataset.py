import pandas as pd
from sklearn.model_selection import train_test_split

from .BaseDataset import BaseDataset

class CSVDataset(BaseDataset):
    def __init__(self, path=None,label='label', name=None):
        self.name = name if name else str(path)
        df = pd.read_csv(path)
        self.y = df[label]
        self.X = df.drop(label, axis=1)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, random_state=0
        )