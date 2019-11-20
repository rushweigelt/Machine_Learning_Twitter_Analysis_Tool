import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold

def get_stratified_k_folds(users, labels, n_splits):
    """
    Performs stratified KFolds split of users

    Takes a list of user ids, labels as argument

    Returns two lists of length n_splits, containing lists of user id's within each fold.
    First list returned is train folds, second list test folds.
    """

    if len(users) != len(labels):
        print("Length of labels does not match length of dataset")
        sys.exit(-1)

    users_labels = pd.DataFrame({'userid':users,'bot':labels})

    user_list = np.unique(users_labels.values, axis=0)

    user_ids = user_list[:,0]
    user_labels = user_list[:, 1]

    skf = StratifiedKFold(n_splits=n_splits, shuffle=True)

    # Split users into train and test sets n_splits times
    train_folds = []
    test_folds = []
    for train_index, test_index in skf.split(user_ids, user_labels):
        train_folds.append(user_ids[train_index])
        test_folds.append(user_ids[test_index])

    return train_folds, test_folds