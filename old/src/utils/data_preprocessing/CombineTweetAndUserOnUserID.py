'''
Rush Weigelt
11.4.19

Preprocessing Step #3

This script exists the combine and label two different, unlabelled dataset to create a training dataset for
regression models. It regulates how many of each data entries we take to account for too-large files.

It can be run in two ways.
1) Edit script directly and run without arguments                       RUN: python3 CombineAndLabel.py
2) Run on command line with two arguments: botfile.csv, genuine.csv     RUN: python3 CombineAndLabel.py bot.csv human.csv

NOTE: Combine files must be located at data > preprocess > combineAndLabel
output file located in 'data' directory
'''

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_validate
from pathlib import Path
import csv
import os
import sys
#Data file names. Files must be csvs and located in the 'data' folder
tweet_filename = 'fake_followers_processed.csv'
user_filename = 'genuine_accounts_processed.csv'
#entryLimit = 150000

#creating directory locations for applicable places in dir
parentDirectory = os.path.abspath(os.path.join(os.getcwd(), "../../../"))
data_folder = os.path.join(parentDirectory, "data", "preprocessed", "combine")
tweet_data = os.path.join(data_folder, tweet_filename)
user_data = os.path.join(data_folder, user_filename)
out_folder = os.path.join(parentDirectory, "data")
#out_path = os.path.splitext(bot_data)[0] + "Combined_with_" + os.path.splitext(genuine_data)[0] + ".csv"

def CombineDataOnID(tweet_file_name, user_file_name):
    out_path = os.path.join(out_folder, "Combined_"+ tweet_filename[:-4]+".csv")
    tweet_data = os.path.join(data_folder, tweet_file_name)
    user_data = os.path.join(data_folder, user_file_name)

    #headers = ['user_id', 'user_createdat', 'description', 'tweet_id', 'tweet_createdat', 'text',  'followerscount',
     #          'friendscount', 'retweeted', 'replycount', 'likecount', 'retweetcount', 'hashtagcount', 'mentioncount', 'urlcount']

    with open(tweet_data, mode='r', encoding='latin-1')as tweet_file:
        reader_tweets = csv.DictReader(x.replace('\0', '') for x in tweet_file)
        first_headers = reader_tweets.fieldnames
        with open(user_data, mode='r', encoding='latin-1')as user_file:
            reader_users = csv.DictReader(x.replace('\0', '') for x in user_file)
            second_headers = reader_users.fieldnames
            combined_headers = first_headers + second_headers
            with open(out_path, 'w', encoding='latin-1', newline='') as combined_file:
                writer = csv.DictWriter(combined_file, fieldnames=combined_headers)
                writer.writeheader()
                for tweet_row in reader_tweets:
                    userid = tweet_row['userid']




    tweet_file.close()
    user_file.close()
    combined_file.close()
    '''
def main():
    if len(sys.argv) < 3:
        CombineAndLabelLimited(bot_data, genuine_data)
    else:
        CombineAndLabelLimited(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()

'''

