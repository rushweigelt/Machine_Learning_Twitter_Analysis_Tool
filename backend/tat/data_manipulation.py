'''
This code existed for pulling data out of the old mongodb, deprecated
'''

#Django imports
from django.db import models
#ML imports
from sklearn.naive_bayes import GaussianNB, BernoulliNB
from sklearn.model_selection import cross_validate, train_test_split, KFold
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from sklearn import metrics
from pymongo import MongoClient
import numpy as np
from joblib import load
from tensorflow.python.keras.initializers import glorot_uniform
from tensorflow.python.keras.models import load_model, model_from_json
#from tensorflow.python.keras.models import load_model, model_from_json
from keras.utils import CustomObjectScope
import re
import nltk
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from dateutil import parser



#Hardcoded function to open our client and look at a specific collection to train our model
#Returns a Pandas Dataframe Object
def read_mongo_data(database, collection):
    client = MongoClient('bvm15.cci.drexel.edu')
    db = client[database]
    df = db[collection]
    df = pd.DataFrame(list(df.find()))
    return df

#Helper function to be used after read_mongo_data: fill nas, convert all columns from strings to numberic
#Returns two pandas dataframe, one a df of our features, the other of our labels
def clean_data_strings_to_ints(dataframe):
    dataframe.fillna(0, inplace=True)
    fieldnames_list = ['followerscount', 'friendscount', 'replycount', 'likecount', 'retweetcount', 'hashtagcount',
                       'urlcount', 'mentioncount']
    x = dataframe[['followerscount', 'friendscount', 'replycount', 'likecount', 'retweetcount', 'hashtagcount', 'urlcount',
              'mentioncount']]
    # convert strings from data into ints
    for item in fieldnames_list:
        x[item] = pd.to_numeric(x[item], errors='coerce')
    # Replace NaNs with 0s for use in ML
    x = x.replace(np.nan, 0, regex=True)
    y = dataframe['label']
    # Convert labels to a list, then convert labels into ints
    # Bots = 0, Genuine = 1
    y_int = y.values.tolist()
    y_int = [int(0) if x == 'bot' else int(1) for x in y_int]
    y_df = pd.DataFrame(y_int)
    return x, y_df

#This cleans the data we get from twitter for numerical analysis.
def clean_twitter_data_strings_to_ints(dataframe):
    dataframe.fillna(0, inplace=True)
    fieldnames_list = ['favoritecount', 'quotecount', 'replycount', 'retweetcount']
    x = dataframe[['favoritecount', 'quotecount', 'replycount', 'retweetcount']]
    # convert strings from data into ints
    for item in fieldnames_list:
        x[item] = pd.to_numeric(x[item], errors='coerce')
    # Replace NaNs with 0s for use in ML
    x = x.replace(np.nan, 0, regex=True)
    x = x.rename(columns={'favoritecount': 'likecount'})
    return x

#Get unlabelled twitter text and clean it in the fashion our lstm was trained on
def clean_twitter_data_text_analysis(df):
    #Clean data exactly as we do before training model
    df.fillna(0, inplace=True)
    df = df.applymap(str)
    df = df[df.apply(lambda x: x != "")]
    ##TAKEN FROM @sabbar
    def clean_text(text):
        # Convert words to lower case and split them
        text = text.lower().split()
        text = " ".join(text)
        text = re.sub(r"[^A-Za-z0-9^,!.\/'+-=]", " ", text)
        text = re.sub(r"what's", "what is ", text)
        text = re.sub(r"\'s", " ", text)
        text = re.sub(r"\'ve", " have ", text)
        text = re.sub(r"n't", " not ", text)
        text = re.sub(r"i'm", "i am ", text)
        text = re.sub(r"\'re", " are ", text)
        text = re.sub(r"\'d", " would ", text)
        text = re.sub(r"\'ll", " will ", text)
        text = re.sub(r",", " ", text)
        text = re.sub(r"\.", " ", text)
        text = re.sub(r"!", " ! ", text)
        text = re.sub(r"\/", " ", text)
        text = re.sub(r"\^", " ^ ", text)
        text = re.sub(r"\+", " + ", text)
        text = re.sub(r"\-", " - ", text)
        text = re.sub(r"\=", " = ", text)
        text = re.sub(r"'", " ", text)
        text = re.sub(r"(\d+)(k)", r"\g<1>000", text)
        text = re.sub(r":", " : ", text)
        text = re.sub(r" e g ", " eg ", text)
        text = re.sub(r" b g ", " bg ", text)
        text = re.sub(r" u s ", " american ", text)
        text = re.sub(r"\0s", "0", text)
        text = re.sub(r" 9 11 ", "911", text)
        text = re.sub(r"e - mail", "email", text)
        text = re.sub(r"j k", "jk", text)
        text = re.sub(r"\s{2,}", " ", text)
        ## Stemming
        text = text.split()
        stemmer = nltk.SnowballStemmer('english')
        stemmed_words = [stemmer.stem(word) for word in text]
        text = " ".join(stemmed_words)
        return text
    ##end taken from @sabbar
    # apply clean text to our tweet data
    df[0] = df[0].map(lambda x: clean_text(x))
    # limit vocab size, then tokenize as a preprocessing step
    vocab_size = 20000
    tokenizer = Tokenizer(num_words=vocab_size)
    tokenizer.fit_on_texts(df[0])
    sequences = tokenizer.texts_to_sequences(df[0])
    data = pad_sequences(sequences, maxlen=50)
    return data


def friends_followers_ratio(friends, followers):
    """
    Function for getting the normalized friends to followers ratio, as specified in:
    Wang, Haining. "Detecting Automation of Twitter Accounts: Are You a Human, Bot or Cyborg?"
    IEEE Transactions on Dependable and Secure Computing. November 2012.
    Args:
        friends - 1xN numpy array of friend counts
        followers - 1xN numpy array of follower counts
    Returns:
        1xN numpy array containing friends to followers ratios
    """

	# Zero division handling adapted from DStauffman's solution at:
	# https://stackoverflow.com/a/37977222
    if friends + followers != 0:
        a = np.divide(followers, (friends + followers))
    else:
        return 0
    return a


def account_age(account_createdat, tweet_createdat):
    """
    Function for getting the account age, as specified in:
    Yang, Kai-Cheng. "Scalable and Generalizable Social Bot Detection through Data Selection"
    arXiv, November 2019
    Args:
        account_createdat - 1xN numpy array of account creation dates in string format
        tweet_createdat - 1xN numpy array of tweet creation dates in string format
    Returns:
        1xN numpy array containing the account age in hours
    """
    if account_createdat or tweet_createdat == "":
        acc_age = 1
        return acc_age

    else:
        # Remove timezone info
        rem_tz = np.vectorize(lambda x: re.sub(r"\s\+[0-9]{4}\s", " ", x))
        account_createdat = rem_tz(account_createdat)
        tweet_createdat = rem_tz(tweet_createdat)

        # Parse date from string
        dt_convert = np.vectorize(lambda x: parser.parse(x))

        account_createdat = dt_convert(account_createdat)
        tweet_createdat = dt_convert(tweet_createdat)

        # Find the age by taking difference of tweet and acc creation dates
        acc_age = tweet_createdat - account_createdat

        # Convert the time delta object to hours
        hours_convert = np.vectorize(lambda x: x.total_seconds() / 3600)
        acc_age = hours_convert(acc_age)

        return acc_age


def growth_rate(feature, acc_age):
	"""
		Function for getting the growth rate of a feature as specified in:
		Yang, Kai-Cheng. "Scalable and Generalizable Social Bot Detection through Data Selection"
		arXiv, November 2019
		Args:
			feature - 1xN numpy array containing numerical feature values
			account_createdat - 1xN numpy array of account creation dates in string format
			tweet_createdat - 1xN numpy array of tweet creation dates in string format
		Returns:
			1xN numpy array containing growth rate per hour of the feature
		"""

	feature_gr = np.divide(feature, acc_age)

	return feature_gr
