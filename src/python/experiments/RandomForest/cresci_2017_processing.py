"""
Script for converting the Cresci-2017 datasets to our standardized
format and importing it to other scripts

"""


import pandas as pd

CRESCI_TWEET_COLS = ['user_id', 'retweet_count', 'reply_count', 'favorite_count', 'num_hashtags', 'num_urls', 'num_mentions']

CRESCI_USER_COLS = ['id', 'followers_count',  'friends_count']

CRESCI_USER_COL_MAPPING = { 'id':'userid',
                            'followers_count':'followers_count',
                            'friends_count':'following_count' }

CRESCI_TWEET_COL_MAPPING = {'user_id':'userid',
                            #'tweet_text':'tweet_text',
                            'retweet_count':'retweet_count',
                            'favorite_count':'like_count',
                            'reply_count':'reply_count',
                            'num_hashtags':'hashtag_count',
                            'num_urls':'url_count',
                            'num_mentions':'mention_count'}

CRESCI_TWEET_DTYPES = {'id': str,
                       'user_id': str,
                            #'tweet_text':'tweet_text',
                            'retweet_count':float,
                            'favorite_count':float,
                            'reply_count':float,
                            'num_hashtags':float,
                            'num_urls':float,
                            'num_mentions':float}

CRESCI_USER_DTYPES = {'id': str,
                      'followers_count': float,
                      'friends_count': float}



def reformat_user_data(user_data):
    cols = CRESCI_USER_COLS

    # Extract relevant columns
    user_data = user_data[cols]

    # Change column data types
    #user_data = user_data.astype('int32')

    # Rename columns to Standard Field format
    user_data = user_data.rename(CRESCI_USER_COL_MAPPING, axis='columns')

    return user_data


def reformat_tweet_data(tweet_data):
    cols = CRESCI_TWEET_COLS

    # Filter columns
    tweet_data = tweet_data[cols]

    # Change column types
    #tweet_data = tweet_data.astype('int32')

    # Rename columns to Standard Field format
    tweet_data = tweet_data.rename(CRESCI_TWEET_COL_MAPPING, axis='columns')

    return tweet_data

def combine_users_tweets(user_data, tweet_data):
    dataset = pd.merge(tweet_data, user_data, on='userid')

    return dataset

def get_data(data_dir):
    tweet_data = pd.read_csv(data_dir + r'\tweets.csv', usecols=CRESCI_TWEET_COLS,
                             dtype=CRESCI_TWEET_DTYPES)

    tweet_data = reformat_tweet_data(tweet_data)

    tweet_data = tweet_data.drop_duplicates()


    user_data = pd.read_csv(data_dir + r'\users.csv', usecols=CRESCI_USER_COLS,
                            dtype=CRESCI_USER_DTYPES)

    user_data = reformat_user_data(user_data)

    # Merge tweet and user data
    dataset = combine_users_tweets(user_data, tweet_data)

    return dataset
