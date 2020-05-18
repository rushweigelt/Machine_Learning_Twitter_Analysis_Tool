"""
Reference: https://towardsdatascience.com/multi-class-text-classification-with-lstm-1590bee1bd17
https://github.com/susanli2016/NLP-with-Python/blob/master/Multi-Class%20Text%20Classification%20LSTM%20Consumer%20complaints.ipynb

"""

import numpy as np
import re
from keras.preprocessing.text import hashing_trick, text_to_word_sequence
from keras.preprocessing import sequence
from nltk.corpus import stopwords  # MUST BE IMPORTED SEPARATELY (call nltk.download())

# TEXT CLEANING CONSTANTS
USER = re.compile('@[A-Za-z0-9]+')

# Hyperlink regexp from https://stackoverflow.com/a/17773849
HYPERLINK = re.compile('(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}'
                       '|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|'
                       '(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})')

HASHTAG = re.compile('#[^ ]+\s*')
ACCEPTED_CHARS = re.compile('[^0-9a-zA-Z@#\' ]')
STOPWORDS = set(stopwords.words('english'))
SEQ_FILTERS = '!”$%&()*+,-./:;<=>?[\\]^_`{|}~\t\n'


def clean_tweet(tweet):

    # Replace @<username> with @USER
    c_tweet = USER.sub('@USER ', tweet)

    # Replace hyperlinks with "hyperlink"
    c_tweet = HYPERLINK.sub('HYPERLINK ', c_tweet)

    # Replace hashtags with '#hashtag'
    c_tweet = HASHTAG.sub('#HASHTAG ', c_tweet)

    # Replace non-accepted symbols & chars
    c_tweet = ACCEPTED_CHARS.sub('', c_tweet)

    tweet_words = text_to_word_sequence(c_tweet, filters=SEQ_FILTERS, lower=False)

    tweet_words = [word for word in tweet_words if not word.lower() in STOPWORDS]

    if len(tweet_words) < 1:
        return ""

    cleaned_tweet = " ".join(tweet_words)

    return cleaned_tweet


def tokenize(text_data, vocab_size, max_len):
    encoded_tweets = []

    for i in range(len(text_data)):
        text = text_data[i]

        if text == "":
            encoded_tweets.append(np.zeros(max_len))
            continue

        encoded_tweet = hashing_trick(text, vocab_size, hash_function='md5', filters=SEQ_FILTERS, lower=False)

        encoded_tweet = sequence.pad_sequences([encoded_tweet], maxlen=max_len, padding="post", truncating="post")[0]

        encoded_tweets.append(encoded_tweet)

    return np.asarray(encoded_tweets)


def process_text(tweet_data, vocab_size, max_len):
    v_clean = np.vectorize(clean_tweet)

    clean_text = v_clean(tweet_data["text"].values)

    encoded_text = tokenize(clean_text, vocab_size, max_len)

    return encoded_text



