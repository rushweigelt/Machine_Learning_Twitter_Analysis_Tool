import pandas as pd
import csv

DATA_DIR = r"G:\Documents\Drexel\Final_Project\cresci_2015_dataset\FSF"

#CRESCI_TWEET_COLS = ['user_id', 'retweet_count', 'reply_count', 'favorite_count', 'num_hashtags', 'num_urls', 'num_mentions']

CRESCI_USER_COLS = ['id', 'name', 'description', 'screen_name', 'followers_count',  'friends_count', 'favourites_count', 'listed_count', 'statuses_count','lang', 'location', 'default_profile', 'default_profile_image', 'verified', 'created_at']

CRESCI_USER_COL_MAPPING = { 'id':'userid',
                            'followers_count':'followerscount',
                            'friends_count':'followingcount',
                            'name':'name',
                            'screen_name':'screenname',
                            'lang':'account_lang',
                            'location':'location',
                            'default_profile_image':'defaultprofileimage',
                            'default_profile':'defaultprofile',
                            'created_at':'account_createdat',
                            'statuses_count':'statusescount',
                            'favourites_count':'favouritescount',
                            'listed_count':'listedcount'
                            }

CRESCI_TWEET_COL_MAPPING = {'id':'tweetid',
                            'user_id':'userid',
                            'retweet_count':'retweetcount',
                            'favorite_count':'likecount',
                            'reply_count':'replycount',
                            'num_hashtags':'hashtagcount',
                            'num_urls':'urlcount',
                            'num_mentions':'mentioncount',
                            'timestamp':'tweet_createdat'}



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

    dataset.drop(columns=['created_at'], axis=1)

    print(len(dataset))

    return dataset

if __name__ == "__main__":

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

        with open(DATA_DIR + '/FSF_processed.csv', 'a', encoding='utf-8', newline='') as f:
            data.to_csv(f, header=header, index=False, encoding='utf-8')

    file_len = len(pd.read_csv(DATA_DIR + "/FSF_processed.csv", usecols=["userid"])) + 1
    print("Num. Tweets: %d" % file_len)