import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from pathlib import Path

from Models import SklearnModel

class GaussianNBModel(SklearnModel):
    def __init__(self):
        super()
        self.model = GaussianNB()

if __name__ == "__main__":
    data_folder = Path("./data")
    data_path = data_folder/"CombinedEnglishFakeFollowersAndGenuineUsers_190kEach.csv"
    data = pd.read_csv(data_path, encoding='latin-1')
    data.fillna(0, inplace=True)
    x = data[['reply_count', 'like_count', 'retweet_count', 'hashtag_count', 'url_count', 'mention_count']]
    y = data['label']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.35,  random_state=0)
    model = GaussianNBModel()
