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
bot_data_file_name = 'russian_tweets.csv'
bot_data_file_name2 = 'china_tweets.csv'
bot_data_file_name3 = 'ira_tweets.csv'
bot_data_file_name4 = 'iran_tweets.csv'
bot_files_names = [bot_data_file_name, bot_data_file_name2, bot_data_file_name3, bot_data_file_name4]
genuine_data_file_name = 'genuine_accounts_processed.csv'
entryLimit = 150000
botLimit = int(entryLimit/4)

#creating directory locations for applicable places in dir
parentDirectory = os.path.abspath(os.path.join(os.getcwd(), "../../../"))
data_folder = os.path.join(parentDirectory, "data", "preprocessed", "combineAndLabel")
bot_data = os.path.join(data_folder, bot_data_file_name)
genuine_data = os.path.join(data_folder, genuine_data_file_name)
out_folder = os.path.join(parentDirectory, "data")
#out_path = os.path.splitext(bot_data)[0] + "Combined_with_" + os.path.splitext(genuine_data)[0] + ".csv"

def CombineAndLabelLimited(genuineDataName):
    out_path = os.path.join(out_folder, "combined_multi_bot_and_genuine_"+str(entryLimit/1000)+"k_split.csv")
    #bot_data = os.path.join(data_folder, botDataName)
    genuine_data = os.path.join(data_folder, genuineDataName)

    headers = ['user_id', 'user_createdat', 'description', 'tweet_id', 'tweet_createdat', 'text',  'followerscount',
               'friendscount', 'retweeted', 'replycount', 'likecount', 'retweetcount', 'hashtagcount', 'mentioncount', 'urlcount', 'label']

    with open(out_path, 'w', encoding='latin-1', newline='') as combined_file:
        csv_writer = csv.DictWriter(combined_file, fieldnames=headers)
        csv_writer.writeheader()
        for file in bot_files_names:
            bot_data = os.path.join(data_folder, file)
            with open(bot_data, mode='r', encoding='latin-1')as bot_file:
                csv_reader = csv.DictReader(bot_file)
                i = 0
                for row in csv_reader:
                    new_row = {'user_id' : row['userid'], 'user_createdat' : row['account_creation_date'], 'description' : row['user_profile_description'],
                               'tweet_id' : row['tweetid'], 'tweet_createdat' : row['tweet_time'], 'text' : row['tweet_text'],
                               'followerscount' : row['follower_count'], 'friendscount' : row['following_count'], 'retweeted' : row['is_retweet'],
                               'replycount' : row['reply_count'], 'likecount' : row['like_count'], 'retweetcount' : row['retweet_count'],
                               'hashtagcount' : row['hashtag_count'], 'mentioncount' : row['mention_count'], 'urlcount' : row['url_count'],
                               'label' : 'bot'}
                    csv_writer.writerow(new_row)
                    i += 1
                    if i >= botLimit:
                        print("Done adding bot data to combined data file from " + str(file))
                        break
        print("Done adding bot data to combined data file.")
        with open(genuine_data, mode='r', encoding='latin-1')as genuine_file:
            csv_reader_gen = csv.DictReader(x.replace('\0', '') for x in genuine_file)
            j = 0
            '''
            print(genuine_data)
            print(csv_reader_gen.fieldnames)
            print(next(csv_reader_gen))
            '''
            for row2 in csv_reader_gen:
                new_row_gen = {'user_id' : row2['userid'], 'user_createdat' : row2['account_createdat'], 'description' : row2['description'],
                               'tweet_id' : row2['tweetid'], 'tweet_createdat' : row2['created_at'], 'text' : row2['text'],
                               'followerscount' : row2['followerscount'], 'friendscount' : row2['followingcount'], 'retweeted' : row2['retweeted'],
                               'replycount' : row2['replycount'], 'likecount' : row2['favoritecount'], 'retweetcount' : row2['retweetcount'],
                               'hashtagcount' : row2['hashtagcount'], 'mentioncount' : row2['mentioncount'], 'urlcount' : row2['urlcount'],
                                   'label' : 'genuine'}
                csv_writer.writerow(new_row_gen)
                j += 1
                if j >= entryLimit:
                    break
        print("Done adding genuine data to combined data file.")

    genuine_file.close()
    bot_file.close()
    combined_file.close()

def main():
    if len(sys.argv) < 2:
        CombineAndLabelLimited(genuine_data)
    else:
        CombineAndLabelLimited(sys.argv[1])

if __name__ == "__main__":
    main()



