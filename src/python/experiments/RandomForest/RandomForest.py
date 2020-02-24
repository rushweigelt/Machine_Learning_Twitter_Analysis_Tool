"""
RandomForest Classifier for cresci-2017 bot and human datasets
"""


from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import shuffle
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
import numpy as np
import cresci_2017_processing as cp
import k_folds as kf

BOT_DATA = r'G:\Documents\Drexel\Final_Project\Datasets\cresci_2017_dataset\cresci-2017.csv\datasets_full.csv\social_spambots_1.csv\social_spambots_1.csv'
HUMAN_DATA = r'G:\Documents\Drexel\Final_Project\Datasets\cresci_2017_dataset\cresci-2017.csv\datasets_full.csv\genuine_accounts.csv'

COLS = ['retweet_count', 'like_count', 'reply_count', 'hashtag_count', 'url_count', 'mention_count', 'followers_count', 'following_count']

def get_test_train_sets(train_user_ids, test_user_ids, dataset, labels):
    """
    Function for retrieving data for a list of train & test user ids from dataset
    """
    dataset['bot'] = labels

    # Extract records based on user id
    train_set = dataset.loc[dataset['userid'].isin(train_user_ids)]
    test_set = dataset.loc[dataset['userid'].isin(test_user_ids)]

    train_x, train_y = train_set[COLS].copy().values, train_set['bot'].copy().values
    test_x, test_y = test_set[COLS].copy().values, test_set['bot'].copy().values

    # Shuffle data
    train_x, train_y = shuffle(train_x, train_y)
    test_x, test_y = shuffle(test_x, test_y)

    train_y = np.reshape(train_y, (-1, 1))
    test_y = np.reshape(test_y, (-1, 1))

    return train_x, test_x, train_y, test_y

def load_dataset(human_data_dir, bot_data_dir):
    human_data = cp.get_data(human_data_dir)
    bot_data = cp.get_data(bot_data_dir)

    # Create labels: 0 for human, 1 for bot
    human_data_labels = np.zeros(len(human_data)).astype(int)
    bot_data_labels = np.full(len(bot_data), fill_value=1).astype(int)

    # Combine human and bot datasets & labels
    dataset = human_data.append(bot_data, ignore_index=True)
    labels = np.concatenate((human_data_labels, bot_data_labels), axis=0)

    return dataset, labels


def train_model(dataset, labels, model, num_folds):
    # Split data into train and test set
    #train_x, test_x, train_y, test_y = get_train_test_split(dataset, labels)

    # Get num_folds sets of user ids
    train_folds, test_folds = kf.get_stratified_k_folds(dataset['userid'].values, labels, num_folds)

    # Train models
    scores = []
    for i in range(num_folds):
        train_x, test_x, train_y, test_y = get_test_train_sets(train_folds[i], test_folds[i], dataset, labels)

        # Normalize the data by fitting min max scaler to train set, then scaling both train & test set
        minmax_scaler = MinMaxScaler()
        minmax_scaler.fit(train_x)

        train_x = minmax_scaler.transform(train_x)
        test_x = minmax_scaler.transform(test_x)

        model.fit(train_x, train_y.flatten())

        predicted_y = model.predict(test_x)

        score = accuracy_score(test_y.flatten(), predicted_y)

        scores.append(score)

    return scores


def main():
    #model = svm.SVC()
    model = LogisticRegression(verbose=0)
    #model = GaussianNB()
    #model = RandomForestClassifier(n_estimators=20, criterion='gini', verbose=1, max_depth=9)

    dataset, labels = load_dataset(HUMAN_DATA, BOT_DATA)

    scores = train_model(dataset, labels, model, 5)

    for i in range(len(scores)):
        print("Fold %d score: %.2f" % (i, scores[i]))

    print("Avg. score: %.2f" % (sum(scores)/len(scores)))



if __name__ == "__main__":
    main()
