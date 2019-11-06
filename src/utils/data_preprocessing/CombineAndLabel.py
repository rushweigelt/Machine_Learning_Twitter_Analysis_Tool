'''
Rush Weigelt
11.4.19

Preprocessing Step #3

This script exists the combine and label two different, unlabelled dataset to create a training dataset for
regression models.

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
bot_data_file_name = 'chinaBotsUnlabelled_counted_StandardizedFieldnames.csv'
genuine_data_file_name = 'genuineUnlabelled_StandardizedFieldnames.csv'

#creating directory locations for applicable places in dir
parentDirectory = os.path.abspath(os.path.join(os.getcwd(), "../../../"))
data_folder = os.path.join(parentDirectory, "data", "preprocessed", "combineAndLabel")
out_folder = os.path.join(parentDirectory, "data")
bot_data = os.path.join(data_folder, bot_data_file_name)
genuine_data = os.path.join(data_folder, genuine_data_file_name)
#out_path = os.path.splitext(bot_data)[0] + "Combined_with_" + os.path.splitext(genuine_data)[0] + ".csv"

#Change this if we must count URLs and
path_for_counting = bot_data

def CombineAndLabel(botDataName, genuineDataName):
    out_path = os.path.join(out_folder, "Combined_" + bot_data_file_name[:-4] + "_AND_" + genuine_data_file_name[:-4] + ".csv")
    bot_data = os.path.join(data_folder, botDataName)
    genuine_data = os.path.join(data_folder, genuineDataName)
    combined_headers = ['tweetid', 'userid', 'tweet', 'reply_count', 'retweet_count', 'hashtag_count', 'url_count', "mention_count", 'label']
    with open(out_path, 'w', encoding='latin-1', newline='') as combined_file:
        csv_writer = csv.DictWriter(combined_file, fieldnames=combined_headers)
        csv_writer.writeheader()
        with open(bot_data, mode='r', encoding='latin-1')as bot_file:
            csv_reader = csv.DictReader(bot_file)
            for row in csv_reader:
                new_row = {'tweetid' : row['tweetid'], 'userid' : row['userid'], 'tweet' : row['tweet_text'], 'reply_count' : row['reply_count'],
                           'retweet_count' : row['retweet_count'], 'hashtag_count' : row['hashtag_count'], 'url_count' : row['url_count'],
                           'mention_count' : row['mention_count'], 'label' : 'bot'}
                csv_writer.writerow(new_row)
            print("Done adding bot data to combined data file.")
        with open(genuine_data, mode='r', encoding='latin-1')as genuine_file:
            csv_reader_gen = csv.DictReader(x.replace('\0', '') for x in genuine_file)
            for row in csv_reader_gen:
                new_row_gen = {'tweetid' : row['tweetid'], 'userid' : row['userid'], 'tweet' : row['tweet_text'], 'reply_count' : row['reply_count'],
                           'retweet_count' : row['retweet_count'], 'hashtag_count' : row['hashtag_count'], 'url_count' : row['url_count'],
                           'mention_count' : row['mention_count'], 'label' : 'genuine'}
                csv_writer.writerow(new_row_gen)
            print("Done adding genuine data to combined data file.")

    genuine_file.close()
    bot_file.close()
    combined_file.close()


def main():
    if len(sys.argv) < 3:
        CombineAndLabel(bot_data, genuine_data)
    else:
        CombineAndLabel(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()


