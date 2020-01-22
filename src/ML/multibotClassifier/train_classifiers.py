"""
Script for training classifiers in the sklearn library on the
multi-bot datasets
"""


import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.utils import shuffle
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, plot_confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn_porter import Porter
import numpy as np
import pandas as pd
import k_folds as kf

DATA_PATH = r'G:\Documents\Drexel\Final_Project\multibot\russian_bot_genuine_users_300k_each.csv'

DATA_COLS = ['user_id', 'followerscount','friendscount','replycount','likecount','retweetcount','hashtagcount','mentioncount','urlcount','bot']

TRAIN_COLS = ['followerscount','friendscount','replycount','likecount','retweetcount','hashtagcount','mentioncount','urlcount']


DTYPES = {
            'user_id':str,
            'retweetcount':float,
            'likecount':float,
            'followerscount':float,
            'friendscount':float,
            'replycount':float,
            'hashtagcount':float,
            'urlcount':float,
            'mentioncount':float,
            'bot':int
          }

def get_test_train_sets(train_user_ids, test_user_ids, dataset):
    """
    Function for retrieving data for a list of train & test user ids from dataset
    """

    # Extract records based on user id
    train_set = dataset.loc[dataset['user_id'].isin(train_user_ids)]
    test_set = dataset.loc[dataset['user_id'].isin(test_user_ids)]

    # Extract features to be included in training
    train_x, train_y = train_set[TRAIN_COLS].copy().values, train_set['bot'].copy().values
    test_x, test_y = test_set[TRAIN_COLS].copy().values, test_set['bot'].copy().values

    # Remove NaN entries
    train_x = np.nan_to_num(train_x)
    test_x = np.nan_to_num(test_x)

    # print(np.count_nonzero(np.isnan(train_x)))

    # Shuffle data
    train_x, train_y = shuffle(train_x, train_y)
    test_x, test_y = shuffle(test_x, test_y)

    train_y = np.reshape(train_y, (-1, 1))
    test_y = np.reshape(test_y, (-1, 1))

    return train_x, test_x, train_y, test_y


def train_model(dataset, num_folds, experiment_name):
    user_ids = dataset['user_id'].values
    labels = dataset['bot'].values

    # Get num_folds sets of user ids
    train_folds, test_folds = kf.get_stratified_k_folds(user_ids, labels, num_folds)

    # Train models
    scores = []
    for i in range(num_folds):
        #model = RandomForestClassifier(n_estimators=100, criterion='gini', verbose=1)
        #model = AdaBoostClassifier()
        model = KNeighborsClassifier()
        #model = MLPClassifier((32, 32), solver='adam', verbose=1, max_iter=50)
        #model = GaussianNB()

        train_x, test_x, train_y, test_y = get_test_train_sets(train_folds[i], test_folds[i], dataset)

        # Normalize the data by fitting scaler to train set, then scaling both train & test set
        #minmax_scaler = MinMaxScaler()
        scaler = StandardScaler()
        scaler.fit(train_x)

        train_x = scaler.transform(train_x)
        test_x = scaler.transform(test_x)

        model.fit(train_x, train_y.flatten())

        predicted_y = model.predict(test_x)

        score = accuracy_score(test_y.flatten(), predicted_y)

        print(("Fold %d class distribution: %.2f bots, %.2f humans" % (i, len(train_y[train_y == 1]) / len(train_y), len(train_y[train_y == 0]) / len(train_y))))

        cm_plot = plot_confusion_matrix(model, test_x, test_y, cmap=plt.cm.Blues, normalize='true')
        cm_plot.ax_.set_title(("Fold-%d" % i))
        plt.savefig(experiment_name + "_fold-" + str(i) + ".jpg")

        # Export model to file
        porter = Porter(model, language='js')
        output = porter.export()
        model_file = open(experiment_name + "_fold-" + str(i) + ".js",'w')
        model_file.write(output)

        scores.append(score)

    return scores


def load_dataset(data_dir):
    dataset = pd.read_csv(data_dir, usecols=DATA_COLS, dtype=DTYPES)

    return dataset


def main():
    # model = svm.SVC()
    #model = LogisticRegression(verbose=0)
    # model = GaussianNB()
    # model = RandomForestClassifier(n_estimators=20, criterion='gini', verbose=1, max_depth=9)
    dataset = load_dataset(DATA_PATH)

    scores = train_model(dataset, 5, "GaussNaiveBayes")

    for i in range(len(scores)):
        print("Test fold", i, "score:", scores[i])

if __name__ == "__main__":
    main()
