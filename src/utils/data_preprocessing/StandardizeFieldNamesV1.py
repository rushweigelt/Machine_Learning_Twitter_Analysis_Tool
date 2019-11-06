'''
Script will then swap incorrect fieldnames for our standardized ones.

by Rush Weigelt

Script can be run in two ways:
1) Commmand Line: argument 1 = filename.csv (must be in data>fieldnameFixFiles folder) argument 2 =list,of,incorrect,fieldnames,in,proper,order,listed,below
2) Change variables in script dp = data file name (must be in data > fieldnameFixFiles folder) and change INCORRECT VALUES section
3) Can run TEST files by python3 StandardizeFieldNamesV1.py test in CommandLine

order:
tweetid, userid, follower_count, following_count, account_date, user_description, text, reply_count, like_count, retweet_count
hashtag_count, mention_count, url_count
'''

from pathlib import Path
import csv
import pandas as pd
import os
import sys

parentDirectory = os.path.abspath(os.path.join(os.getcwd(), "../../../"))

#filename for file we want to augment. Only used if file is called without command line arugments
dp = "fake_bad_headers_test.csv"

#INCORRECT VALUES
#ONLY USED IF SCRIPT RUNS WITHOUT ARGUMENTS
#User Vars
tweetid_wrong = 'twetid'
userid_wrong = 'usrid'
follower_count_wrong = 'folr_cnt'
following_count_wrong = 'foling_cnt'
account_creation_date_wrong = 'acnt_date'
user_profile_description_wrong = 'usr_dsc'
#Tweet Vars
tweet_text_wrong = 'text'
reply_count_wrong = 'rply_cnt'
like_count_wrong = 'like_cnt'
retweet_count_wrong = 'retweet_count'
hashtag_count_wrong = 'has_count'
mention_count_wrong = 'mention_cnt'
url_count_wrong = 'url_cnt'
#Create a list of the above vars
generic_wrong_list = [tweetid_wrong, userid_wrong, follower_count_wrong, following_count_wrong, account_creation_date_wrong,
                  user_profile_description_wrong, tweet_text_wrong, reply_count_wrong, like_count_wrong,
                  retweet_count_wrong, hashtag_count_wrong, mention_count_wrong, url_count_wrong]


# Correct Values, DO NOT CHANGE
tweetid_correct = 'tweetid'
userid_correct = 'userid'
follower_count_correct = 'follower_count'
following_count_correct = 'following_count'
account_creation_date_correct = 'account_creation_date'
user_profile_description_correct = 'user_profile_description'
# Tweet Vars
tweet_text_correct = 'tweet_text'
reply_count_correct = 'reply_count'
like_count_correct = 'like_count'
retweet_count_correct = 'retweet_count'
hashtag_count_correct = 'hashtag_count'
mention_count_correct = 'mention_count'
url_count_correct = 'url_count'
# make a correct list to make iterating easier
correct_list = [tweetid_correct, userid_correct, follower_count_correct, following_count_correct,
                account_creation_date_correct,
                user_profile_description_correct, tweet_text_correct, reply_count_correct, like_count_correct,
                retweet_count_correct,
                hashtag_count_correct, mention_count_correct, url_count_correct]


def StandardizeFields(filename, list_of_incorrect_fieldnames_in_proper_order):
    # path variables
    data_folder = os.path.join(parentDirectory, "data", "fieldnameFixFiles")
    # append give filename to path
    data_path = os.path.join(data_folder, filename)
    #print(data_path)
    # output file name just adds _modified to original title
    out_path = os.path.splitext(data_path)[0] + "_modified.csv"
    #get wrong list from func call
    wrong_list = list_of_incorrect_fieldnames_in_proper_order
    # open offending csv and reorder columns to match what we need.
    with open(data_path, mode='r', encoding='latin-1') as csv_file:
        df = pd.read_csv(csv_file)
        df = df[wrong_list]
        df.to_csv(data_path, index=False)
        csv_file.close()
    # Open original csv
    with open(data_path, mode='r', encoding='latin-1', newline='') as read_file:
        reader = csv.reader(read_file)
        # write correct header, then rest of csv file from read
        with open(out_path, mode='w', encoding='latin-1', newline='') as write_file:
            csv_writer = csv.writer(write_file)
            csv_writer.writerow(correct_list)
            next(reader, None)
            for row in reader:
                csv_writer.writerow(row)
        # close files
        read_file.close()
        write_file.close()
#For main, if arguments are detected try using those, otherwise run with the global vars at the top
def main(*argv):
    if len(sys.argv) >= 3:
        list1 = sys.argv[2].split(',')
        StandardizeFields(sys.argv[1], list1)
    elif len(sys.argv) == 2 and sys.argv[1] == 'test':
        p = os.path.join(parentDirectory, "data", "fieldnameFixFiles", "fake_bad_headers_test.csv")
        StandardizeFields(p, generic_wrong_list)
    else:
        StandardizeFields(dp, generic_wrong_list)

if __name__ == "__main__":
    main()









