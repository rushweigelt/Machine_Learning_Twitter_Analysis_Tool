import numpy as np
import pandas as pd

from .MockDataset import MockDataset
from .CSVDataset import CSVDataset

all_datasets = [
    CSVDataset(
        path='/data/data-sets/processed-data/combined/multi_bot_and_genuine_400k_split.csv',
        types={
            'user_id' : object,
            'user_createdat' : object,
            'description' : object,
            'tweet_id' : np.int32,
            'tweet_createdat' : object,
            'text' : object,
            'followerscount' : np.int32,
            'friendscount' : np.int32,
            'retweeted' : np.float64,
            'replycount' : np.float64,
            'likecount' : np.float64,
            'retweetcount' : np.float64,
            'hashtagcount' : np.int32,
            'mentioncount' : np.int32,
            'urlcount' : np.int32,
            'label' : object,
        },
        parse_dates=[1,4],
        date_parser=lambda col: pd.to_datetime(col, utc=True),
    ),
]