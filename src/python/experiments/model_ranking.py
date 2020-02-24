import csv
from pprint import pprint
import re

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline

from ML.model_selection import ModelRanking

DATASET = "sentiment140"
DATASET_PREFIX = "../dataset"
URL_REGEX = re.compile("https?://.*")
USERNAME_REGEX = re.compile("@[A-Za-z0-9_]+")


def ReplaceURLsUsernames(tweet):
    return re.sub(URL_REGEX, "URL", re.sub(USERNAME_REGEX, "USERNAME", tweet))


def main():
    with open(
        f"{DATASET_PREFIX}/{DATASET}/training.csv", encoding="latin-1"
    ) as training_data:
        reader = csv.reader(training_data)
        fields = next(reader)
        training_tweets = tuple(row for row in reader)

    with open(
        f"{DATASET_PREFIX}/{DATASET}/testing.csv", encoding="latin-1"
    ) as testing_data:
        reader = csv.reader(testing_data)
        fields = next(reader)
        testing_tweets = tuple(row for row in reader)

    training_tweets = [
        [row[0], ReplaceURLsUsernames(row[-1])] for row in training_tweets
    ]
    testing_tweets = [[row[0], ReplaceURLsUsernames(row[-1])] for row in testing_tweets]

    training_X = [row[-1] for row in training_tweets]
    training_Y = np.asarray([int(row[0]) for row in training_tweets])

    testing_X = [row[-1] for row in testing_tweets]
    testing_Y = np.asarray([int(row[0]) for row in testing_tweets])

    tfidf = Pipeline(
        [("vectorizer", CountVectorizer()), ("tfidf", TfidfTransformer()),]
    )

    ranker = ModelRanking(
        [
            (
                tfidf,
                (
                    # RandomForestClassifier(n_estimators=3, verbose=1), data is WAY too high-dimensional for this
                    LogisticRegression(verbose=1),
                    MultinomialNB(),
                    LinearSVC(verbose=1),
                ),
            ),
        ]
    )
    ranker.fit(training_X, training_Y)
    print("\nScores:")

    scores_and_models = ranker.score(testing_X, testing_Y)
    pprint(scores_and_models)


if __name__ == "__main__":
    main()
