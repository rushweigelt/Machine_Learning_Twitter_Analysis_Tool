import pandas as pd
import numpy as np
import sys
import csv


EIH_TWEET_COLS = ["userid", "user_screen_name",
                  "user_profile_description",
                  "user_display_name",
                  "user_reported_location",
                  "account_creation_date",
                  "tweetid",
                  "tweet_text",
                  "follower_count",
                  "following_count",
                  "reply_count",
                  "tweet_time",
                  "like_count",
                  "retweet_count",
                  "hashtags",
                  "urls",
                  "user_mentions",
                  "is_retweet",
                  "tweet_client_name",
                  "account_language",
                  "tweet_language",
				  "latitude",
]

EIH_TWEET_DTYPES = {
    "userid": str,
    "user_screen_name": str,
    "user_display_name":str,
    "user_profile_description": str,
    "user_reported_location":str,
    "account_creation_date": str,
    "tweetid": str,
    "tweet_text": str,
    "tweet_time": str,
    "follower_count": float,
    "following_count": float,
    "reply_count": float,
    "like_count": float,
    "retweet_count":float,
    "is_retweet": bool,
    "hashtags": str,
    "urls": str,
    "user_mentions":str,
    "tweet_client_name": str,
	"latitude":str

}

# Mapping of EIH columns to the Standard Format
EIH_COL_MAPPING = {
    "user_screen_name":"screenname",
    "user_display_name":"name",
    "account_creation_date":"account_createdat",
    "user_profile_description":"description",
    "user_reported_location":"location",
    "tweet_time":"tweet_createdat",
    "follower_count":"followerscount",
    "following_count":"friendscount",
    "account_language":"account_lang",
    "tweet_language":"tweet_lang",
    "is_retweet":"retweeted",
    "reply_count":"replycount",
    "retweet_count":"retweetcount",
    "like_count":"likecount",
    "tweet_client_name":"source",
    "tweet_text":"text",
	"latitude":"geoenabled"
    }


def reformat_tweet_data(tweet_data):
    cols = EIH_TWEET_COLS

    # Filter columns
    tweet_data = tweet_data[cols]

    hashtags_data = tweet_data["hashtags"].copy()
    mentions_data = tweet_data["user_mentions"].copy()
    urls_data = tweet_data["urls"].copy()

    mask = pd.isnull(hashtags_data)
    hashtags_data.loc[mask] = ""

    mask = pd.isnull(mentions_data)
    mentions_data.loc[mask] = ""

    mask = pd.isnull(urls_data)
    urls_data.loc[mask] = ""

    # Convert hashtags, urls and mentions fields to counts
    #hashtag_count = np.apply_along_axis(lambda x: float(str(x).count(",")), axis=0, arr=hashtags_data.values)
    #mention_count = np.apply_along_axis(lambda x: float(str(x).count(",")), axis=0, arr=mentions_data.values)
    #url_count = np.apply_along_axis(lambda x: float(str(x).count(",")), axis=0, arr=urls_data.values)

    # Convert hashtags, urls and mentions fields to counts
    c_elems = np.vectorize(count_elems)

    hashtag_count = c_elems(hashtags_data.values)
    mention_count = c_elems(mentions_data.values)
    url_count = c_elems(urls_data.values)

    # Derive geolocation field
    tweet_data["latitude"] = (tweet_data["latitude"] == 'present').astype(int)

    tweet_data = tweet_data.drop(["hashtags", "user_mentions", "urls"], axis=1)

    tweet_data["urlcount"] = url_count
    tweet_data["hashtagcount"] = hashtag_count
    tweet_data["mentioncount"] = mention_count

    tweet_data = tweet_data.rename(EIH_COL_MAPPING, axis='columns')

    tweet_data = tweet_data.drop_duplicates()

    tweet_data = tweet_data.fillna(0.0)

    return tweet_data

def count_elems(x):
    try:
        x = str(x)

        if x != "[]" and x != '':
            elems = 1.0
        else:
            return 0.0

        commas = x.count(",")

        return elems + commas

    except Exception as e:
        return 0


def get_data(data_dir, skiprows, nrows):
    tweet_data = pd.read_csv(data_dir, dtype=str, skiprows=range(1,skiprows),nrows=nrows)

    tweet_data = reformat_tweet_data(tweet_data)

    #print(len(tweet_data))

    return tweet_data

def main():
    # File options
    data_dir = r"G:\Documents\Drexel\Final_Project\EIH"
    data_file = r"china_082019_3_tweets_csv_hashed_part3.csv"
    filename = data_dir + "/" + data_file
    processed_file = "china3_processed.csv"
    append = True # Option for processing multiple files


    file_len = len(pd.read_csv(filename, usecols=["userid"])) + 1
    print("Num. Tweets: %d" % file_len)

    chunk_size = 500000

    for i in range(file_len // chunk_size + 1):
        if i == 0:
            if not append:
                header = True
            else:
                header = False
        else:
            header = False

        skip = i * chunk_size

        if chunk_size > file_len - skip:
            chunk_size = file_len - skip

        print("Skip to %d" % skip)

        data = get_data(filename, skip, chunk_size - 1)

        with open(data_dir + '/' + processed_file, 'a', encoding='utf-8', newline='') as f:

            data.to_csv(f, header=header, index=False, encoding='utf-8')

    file_len = len(
        pd.read_csv(data_dir + "/" + processed_file, usecols=["userid"])) + 1
    print("Num. Tweets in processed file: %d" % file_len)

if __name__ == "__main__":
    main()
