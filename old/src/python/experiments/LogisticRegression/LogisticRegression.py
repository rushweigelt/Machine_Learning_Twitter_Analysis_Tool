from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_validate, train_test_split, KFold
from sklearn.preprocessing import MinMaxScaler
from pathlib import Path
import pandas as pd
import seaborn as sb
from sklearn import metrics
import os

import matplotlib
from dask.distributed import Client
from sklearn.externals import joblib
#path variables
parentDirectory = os.path.abspath(os.path.join(os.getcwd(), "../../../"))
data_folder = os.path.join(parentDirectory, "data")
dp = os.path.join(data_folder, "combined_multi_bot_and_genuine_200k_split.csv")


#Function for test_train_split
def LRTestTrainSplit(data_path):
    data = pd.read_csv(data_path, encoding='latin-1')
    data.fillna(0, inplace=True)
    x = data[['followerscount', 'friendscount', 'replycount', 'likecount', 'retweetcount', 'hashtagcount', 'urlcount', 'mentioncount']]
    y = data['label']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.35,  random_state=0)
    #client = Client(processes=False)
    lr = LogisticRegression()
    #with joblib.parallel_backend('dask'):
    lr.fit(x_train, y_train)
    x_test.fillna(x_test.mean())
    y_predict = lr.predict(x_test)
    confusion_matrix = pd.crosstab(y_test, y_predict, rownames=['Actual'], colnames=['Predicted'])
    print(confusion_matrix)
    matrix = sb.heatmap(confusion_matrix, annot=True)

    print('Accuracy: ', metrics.accuracy_score(y_test, y_predict))

def LR_KFold(data_path):
    data = pd.read_csv(data_path, encoding='latin-1')
    data.fillna(0, inplace=True)
    x = data[['followerscount', 'friendscount', 'replycount', 'likecount', 'retweetcount', 'hashtagcount', 'urlcount', 'mentioncount']]
    y = data['label']
    scaler = MinMaxScaler(feature_range=(0,1))
    #x = scaler.fit_transform(x)
    #y = scaler.fit_transform(y)
    #kf = KFold(n_splits=10, shuffle=True)
    #kf.get_n_splits(x)
    #kf.get_n_splits(y)
    lr = LogisticRegression()
    cv_results = cross_validate(lr, x, y, cv=10)
    print(cv_results['test_score'])


def main():
    LRTestTrainSplit(dp)
    #LR_KFold(dp)
if __name__ == "__main__":
    main()
