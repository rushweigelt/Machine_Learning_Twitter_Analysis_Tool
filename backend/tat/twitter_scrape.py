import tweepy
import csv
import json
import pandas as pd

data = []
tweets_per_pull = 20
tweet_limit = 50

with open('tat/twitter_credentials.json') as cred_data:
    info = json.load(cred_data)
    consumer_key = info['CONSUMER_KEY']
    consumer_secret = info['CONSUMER_SECRET']
    access_key = info['ACCESS_KEY']
    access_secret = info['ACCESS_SECRET']

def get_all_tweets(hashtag):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    #init list to hold tweet data
    all_tweet_data = []
    search = "#"+hashtag
    #Multiple requests of 200 tweets each
    new_tweets = api.search(search, count=tweets_per_pull)
    all_tweet_data.extend(new_tweets)
    #reindex old tweeets
    oldest_tweet = all_tweet_data[-1].id - 1

    while len(new_tweets) != 0:
        # The max_id param will be used subsequently to prevent duplicates
        new_tweets = api.search(search, count=tweets_per_pull, max_id=oldest_tweet)
        # save most recent tweets
        all_tweet_data.extend(new_tweets)
        #print as loading bar
        oldest_tweet = all_tweet_data[-1].id -1
        print("...{} tweets have downloaded so far".format(len(all_tweet_data)))
        if len(all_tweet_data) >= tweet_limit:
            break
    #convert to string
    json_str = json.dumps(all_tweet_data[0]._json)
    #deserialise string into py obj
    parsed = json.loads(json_str)
    #print(tweet.text)
    #print(json.dumps(parsed, indent=4, sort_keys=True))
    formatted_data = [[tweet.user.followers_count, tweet.user.friends_count, tweet.favorite_count,
                       tweet.retweet_count] for tweet in all_tweet_data]
    print(formatted_data)
    return formatted_data


#data = get_all_tweets('NewHampshire')
#print(data)
#formatted_data = [[tweet.id_str, tweet.created_at, tweet.tweet.encode('utf-8')] for tweet in data]


