import pandas as pd
import csv

DATA_DIR = r"G:\Documents\Drexel\Final_Project\cresci-2017.csv\datasets_full.csv\social_spambots_1.csv\social_spambots_1.csv"

CRESCI_TWEET_COLS = ['user_id', 'retweet_count', 'reply_count', 'favorite_count', 'num_hashtags',
                     'num_urls', 'num_mentions', 'created_at', 'source', 'retweeted']

CRESCI_USER_COLS = ['id', 'name', 'description', 'screen_name', 'followers_count',  'friends_count',
                    'favourites_count', 'listed_count', 'statuses_count','lang', 'location', 'geo_enabled',
                    'default_profile', 'default_profile_image', 'verified', 'created_at']

CRESCI_USER_COL_MAPPING = { 'id':'userid',
                            'followers_count':'followerscount',
                            'friends_count':'friendscount',
                            'name':'name',
                            'screen_name':'screenname',
                            'lang':'account_lang',
                            'location':'location',
                            'geo_enabled':'geoenabled',
                            'default_profile_image':'defaultprofileimage',
                            'default_profile':'defaultprofile',
                            'created_at':'account_createdat',
                            'statuses_count':'statusescount',
                            'favourites_count':'favouritescount',
                            'listed_count':'listedcount',
                            'verified':'verified'
                            }

CRESCI_TWEET_COL_MAPPING = {'id':'tweetid',
                            'user_id':'userid',
                            'retweet_count':'retweetcount',
                            'favorite_count':'likecount',
                            'reply_count':'replycount',
                            'num_hashtags':'hashtagcount',
                            'num_urls':'urlcount',
                            'num_mentions':'mentioncount',
                            'created_at':'tweet_createdat',
                            'source':'source'
                            }




def reformat_user_data(user_data):
    user_data = user_data[CRESCI_USER_COLS]

    # Rename columns to Standard Field format
    user_data = user_data.rename(CRESCI_USER_COL_MAPPING, axis='columns')

    return user_data


def reformat_tweet_data(tweet_data):

    # Rename columns to Standard Field format
    tweet_data = tweet_data.rename(CRESCI_TWEET_COL_MAPPING, axis='columns')

    return tweet_data

def combine_users_tweets(user_data, tweet_data):
    dataset = pd.merge(tweet_data, user_data, on='userid')

    return dataset

def get_data(data_dir, skiprows, nrows):
    tweet_data = pd.read_csv(data_dir + r'\tweets.csv', dtype=str, skiprows=range(1,skiprows),nrows=nrows)

    tweet_data = reformat_tweet_data(tweet_data)

    user_data = pd.read_csv(data_dir + r'\users.csv', dtype=str)

    user_data = reformat_user_data(user_data)

    # Merge tweet and user data
    dataset = combine_users_tweets(user_data, tweet_data)

    # dataset.drop(columns=['created_at'], axis=1)

    print(len(dataset))

    return dataset

if __name__ == "__main__":
    processed_name = "SS1_processed.csv"
    file_len = len(pd.read_csv(DATA_DIR+"/tweets.csv", usecols=["id"])) + 1
    print("Num. Tweets: %d" % file_len)

    chunk_size = 500000

    for i in range(file_len//chunk_size + 1):
        if i == 0:
            header = True
        else:
            header = False

        skip = i * chunk_size

        print("Skip to %d" % skip)

        data = get_data(DATA_DIR,skip,chunk_size-1)

        with open(DATA_DIR + '/' + processed_name, 'a', encoding='utf-8', newline='') as f:
            data.to_csv(f, header=header, index=False, encoding='utf-8')

    file_len = len(pd.read_csv(DATA_DIR + '/' + processed_name, usecols=["userid"])) + 1
    print("Num. Tweets: %d" % file_len)