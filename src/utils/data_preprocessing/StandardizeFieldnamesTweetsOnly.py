'''
by Rush Weigelt
11.4.19

Preprocessing Step #2

Script will then swap incorrect fieldnames for our standardized ones. It concerns itself with Tweet-Only data (as opposed to Tweet & User)

Script can be run in two ways:
1) Commmand Line: argument 1 = filename.csv (must be in data>preprocessed>standardizeFieldnames folder) argument 2 =list,of,incorrect,fieldnames,in,proper,order,listed,below
2) Change variables in script dp = data file name (must be in data > preprocessed > standardizeFieldnames folder) and change INCORRECT VALUES section
3) Can run TEST files by python3 StandardizeFieldnamesTweetsAndUserData.py test in CommandLine

order:
tweetid, userid, follower_count, following_count, account_date, user_description, text, reply_count, like_count, retweet_count
hashtag_count, mention_count, url_count

NOTE: data file must be located at data > preprocess > standardizeFieldnames
Output file will be in data > preprocess > combineAndLabel
'''
import csv
import pandas as pd
import os
import sys

#hold the parent directory so we can navigate
parentDirectory = os.path.abspath(os.path.join(os.getcwd(), "../../../"))

#filename for file we want to augment. Only used if file is called without command line arugments
#CHANGE HERE
dp = "english_fake_followers.csv"

#INCORRECT VALUES
#ONLY USED IF SCRIPT RUNS WITHOUT ARGUMENTS
#User Vars
tweetid_wrong = 'id'
userid_wrong = 'user_id'
#Tweet Vars
tweet_text_wrong = 'text'
reply_count_wrong = 'reply_count'
like_count_wrong = 'favorite_count'
retweet_count_wrong = 'retweet_count'
hashtag_count_wrong = 'num_hashtags'
mention_count_wrong = 'num_mentions'
url_count_wrong = 'num_urls'
#Create a list of the above vars
generic_wrong_list = [tweetid_wrong, userid_wrong, tweet_text_wrong, reply_count_wrong, like_count_wrong,
                  retweet_count_wrong, hashtag_count_wrong, mention_count_wrong, url_count_wrong]


# Correct Values, DO NOT CHANGE
tweetid_correct = 'tweetid'
userid_correct = 'userid'
# Tweet Vars
tweet_text_correct = 'tweet_text'
reply_count_correct = 'reply_count'
like_count_correct = 'like_count'
retweet_count_correct = 'retweet_count'
hashtag_count_correct = 'hashtag_count'
mention_count_correct = 'mention_count'
url_count_correct = 'url_count'
# make a correct list to make iterating easier
correct_list = [tweetid_correct, userid_correct, tweet_text_correct, reply_count_correct, like_count_correct,
                retweet_count_correct,
                hashtag_count_correct, mention_count_correct, url_count_correct]

#Standardize the order and spelling of all our fieldnames.
def StandardizeFields(filename, list_of_incorrect_fieldnames_in_proper_order):
    # path variables
    data_folder = os.path.join(parentDirectory, "data", "preprocessed", "standardizeFieldnames")
    # append give filename to path
    data_path = os.path.join(data_folder, filename)
    out_folder = os.path.join(parentDirectory, "data", "preprocessed", "combineAndLabel")
    # output file name just adds _modified to original title
    out_path = os.path.join(out_folder, filename[:-4] + "_StandardizedFieldnames.csv")
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
        print("Finished.\nData File is in data > preprocess > combineAndLabel")
        # close files
        read_file.close()
        write_file.close()


#For main, if arguments are detected try using those, otherwise run with the global vars at the top
def main(*argv):
    if len(sys.argv) >= 3:
        list1 = sys.argv[2].split(',')
        StandardizeFields(sys.argv[1], list1)
    elif len(sys.argv) == 2 and sys.argv[1] == 'test':
        p = os.path.join(parentDirectory, "data", "preprocessed", "standardizeFieldnames", "fake_bad_headers_test.csv")
        StandardizeFields(p, generic_wrong_list)
    else:
        StandardizeFields(dp, generic_wrong_list)

if __name__ == "__main__":
    main()








