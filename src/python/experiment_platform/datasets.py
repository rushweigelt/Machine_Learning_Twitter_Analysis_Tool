"""
Provides various classes for loading datasets from different data stores.
Also contains list of all datasets for the project.
"""
from abc import ABC

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold, StratifiedKFold
from sklearn.datasets import load_breast_cancer


class BaseDataset(ABC):
    """
    Abstract base class for Datasets.
    """

    def __init__(self):
        self.X = None
        self.y = None
        self.cv = None
        self.loaded = False

    def load(self):
        """
        Load the dataset into memory. X, y, and cv may be None before this is called
        """
        self.loaded = True


class CSVDataset(BaseDataset):
    """
    Dataset loaded from a CSV.
    """

    def __init__(
        self, path=None, label="label", name=None, types=None, group_by=None, **kwargs
    ):
        self.name = name if name else str(path).split("/")[-1]
        self.loaded = False
        self.group_by = group_by
        self.load = lambda: self.__load(path, label, types, group_by, **kwargs)

    def __load(self, path, label, types, group_by, **kwargs):
        if self.loaded:
            return
        super().load()

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


class MockDataset(BaseDataset):
    """
    Mock dataset using sklearn breast cancer dataset.
    """

    def __init__(self):
        self.name = "Mock Dataset"

    def load(self):
        if self.loaded:
            return
        super().load()
        self.X, self.y = load_breast_cancer(return_X_y=True)
        self.cv = StratifiedKFold().split(self.X, self.y)


# TODO: Implement SQL/Mongo datasets (check Lucas' branch)
# TODO: Add additional CSV datasets

ALL_DATASETS = [
    CSVDataset(
        path="/data/data-sets/processed-data/combined/multi_bot_and_genuine_400k_split.csv",
        types={
            "user_id": object,
            "user_createdat": object,
            "description": object,
            "tweet_id": np.int32,
            "tweet_createdat": object,
            "text": object,
            "followerscount": np.int32,
            "friendscount": np.int32,
            "retweeted": np.float64,
            "replycount": np.float64,
            "likecount": np.float64,
            "retweetcount": np.float64,
            "hashtagcount": np.int32,
            "mentioncount": np.int32,
            "urlcount": np.int32,
            "label": object,
        },
        group_by="user_id",
        parse_dates=[1, 4],
        date_parser=lambda col: pd.to_datetime(col, utc=True),
    ),
]
