import csv
import re

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

DATASET = 'sentiment140'
URL_REGEX = re.compile('https?://.*')
USERNAME_REGEX = re.compile('@[A-Za-z0-9_]+')

def replace_urls_usernames(tweet):
    return re.sub(URL_REGEX, 'URL', re.sub(USERNAME_REGEX, 'USERNAME', tweet))

with open(f'{DATASET}_training.csv', encoding='latin-1') as training_data:
    reader = csv.reader(training_data)
    fields = next(reader)
    training_tweets = tuple(row for row in reader)

with open(f'{DATASET}_testing.csv', encoding='latin-1') as testing_data:
    reader = csv.reader(testing_data)
    fields = next(reader)
    testing_tweets = tuple(row for row in reader)

training_tweets = [[row[0], replace_urls_usernames(row[-1])] for row in training_tweets]
testing_tweets = [[row[0], replace_urls_usernames(row[-1])] for row in testing_tweets]

training_X = [row[-1] for row in training_tweets]
training_Y = np.asarray([int(row[0]) for row in training_tweets])

testing_X = [row[-1] for row in testing_tweets]
testing_Y = np.asarray([int(row[0]) for row in testing_tweets])

text_clf = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', MultinomialNB()),
]).fit(training_X, training_Y)

predicted = text_clf.predict(testing_X)
accuracy = np.mean(predicted == testing_Y)
print(accuracy)
