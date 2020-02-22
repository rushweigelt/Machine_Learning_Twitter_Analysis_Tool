from .MockDataset import MockDataset
from .CSVDataset import CSVDataset

all_datasets = [
    CSVDataset(path='/data/data-sets/processed-data/combined/multi_bot_and_genuine_400k_split.csv')
]