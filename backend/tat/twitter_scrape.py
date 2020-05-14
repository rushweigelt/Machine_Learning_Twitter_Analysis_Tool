'''
Scrape Data from Twitter utilizing the Tweepy library.

Rush Weigelt

2/20/20
'''

import tweepy
import csv
import json
import pandas as pd
import requests
from data_manipulation import friends_followers_ratio, account_age, growth_rate
import numpy as np

#empty list for data, and numbers for how many tweets we pull at a time, and what our total limit is.
data = []
tweets_per_pull = 10
tweet_limit = 50

#Store credentials in a json, make sure json isn't in public repo (gitignore)
with open('tat/twitter_credentials.json') as cred_data:
    info = json.load(cred_data)
    consumer_key = info['CONSUMER_KEY']
    consumer_secret = info['CONSUMER_SECRET']
    access_key = info['ACCESS_KEY']
    access_secret = info['ACCESS_SECRET']

#Grab our tweets by the user-inputted hashtag
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
    #Natural: followers Count, friendsCount, replyCount, likeCount, retweetCount, hashtagCount, mentionCount, urlCounr
    #Engineered: accountrep, friends_growthrate, followers_growthrate
    formatted_data = [[tweet.user.followers_count, tweet.user.friends_count, 0, tweet.favorite_count,
                       tweet.retweet_count, len(tweet.entities.get("hashtags")), len(tweet.entities.get("user_mentions")),
                       len(tweet.entities.get("urls")),
                       #accountrep
                       friends_followers_ratio(np.array(tweet.user.friends_count), np.array(tweet.user.followers_count)),
                       #friends growth rate
                       growth_rate(np.array(tweet.user.friends_count), account_age(np.array(tweet.user.created_at), np.array(tweet.created_at))),
                       #followers_growthrate
                       growth_rate(np.array(tweet.user.followers_count), account_age(np.array(tweet.user.created_at), np.array(tweet.created_at)))
                       ] for tweet in all_tweet_data]
    text_data = [[tweet.text] for tweet in all_tweet_data]
    #request for twitter embedding
    tweet_reconstruct = [[tweet.user.screen_name, tweet.id_str] for tweet in all_tweet_data]
    #tweet_request = requests.get("https://publish.twitter.com/oembed?url=https://twitter.com/" +all_tweet_data[0].user.screen_name +"/status/" + all_tweet_data[0].id_str + "&omit_script=true")
    #tweet_json = tweet_request.json()
    #tweet_html = tweet_json['html']
    #print(formatted_data)
    #print(text_data)
    tweet_loc_verified = [[tweet.user.verified, tweet.user.location, tweet.geo] for tweet in all_tweet_data]
    #print("Verified and locations:")
    #print(tweet_loc_verified)

    return formatted_data, tweet_reconstruct, tweet_loc_verified


#data = get_all_tweets('NewHampshire')
#print(data)
#formatted_data = [[tweet.id_str, tweet.created_at, tweet.tweet.encode('utf-8')] for tweet in data]


def get_twitter_data_lstm(hashtag):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # init list to hold tweet data
    all_tweet_data = []
    search = "#" + hashtag
    # Multiple requests of 200 tweets each
    new_tweets = api.search(search, count=tweets_per_pull)
    all_tweet_data.extend(new_tweets)
    # reindex old tweeets
    oldest_tweet = all_tweet_data[-1].id - 1

    while len(new_tweets) != 0:
        # The max_id param will be used subsequently to prevent duplicates
        new_tweets = api.search(search, count=tweets_per_pull, max_id=oldest_tweet)
        # save most recent tweets
        all_tweet_data.extend(new_tweets)
        # print as loading bar
        oldest_tweet = all_tweet_data[-1].id - 1
        print("...{} tweets have downloaded so far".format(len(all_tweet_data)))
        if len(all_tweet_data) >= tweet_limit:
            break
    # convert to string
    #uncomment to see what the json looks like in an organized fashion
    #json_str = json.dumps(all_tweet_data[0]._json)
    # deserialise string into py obj
    #parsed = json.loads(json_str)
    # print(tweet.text)
    #print(json.dumps(parsed, indent=4, sort_keys=True))
    formatted_data = [[tweet.text] for tweet in all_tweet_data]
    tweet_reconstruct = [[tweet.user.screen_name, tweet.id_str] for tweet in all_tweet_data]
    tweet_loc_verified = [[tweet.user.verified, tweet.user.location, tweet.geo] for tweet in all_tweet_data]
    #print("Verified and locations:")
    #print(tweet_loc_verified)
    #text_data = [[tweet.text] for tweet in all_tweet_data]
    return formatted_data, tweet_reconstruct, tweet_loc_verified