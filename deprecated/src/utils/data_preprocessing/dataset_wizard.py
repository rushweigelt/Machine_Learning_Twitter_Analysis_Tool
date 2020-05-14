import pandas as pd
import numpy as np
import random

processed_file = r'G:\Documents\Drexel\Final_Project\russia_spam_v_multihumans_600k.csv'

cols = ['userid',	'screenname',	'description',	'name',	'location',	'account_createdat',	'tweetid',	'text',
		'followerscount',	'friendscount',	'replycount',	'tweet_createdat',	'likecount',	'retweetcount',
		'source',	'account_lang',	'geoenabled',	'urlcount',	'hashtagcount',
		'mentioncount'] # 'retweeted',


dataset_list = [
	r'G:\Documents\Drexel\Final_Project\cresci-2017.csv\datasets_full.csv\genuine_accounts.csv\genuine_users_processed.csv',
	#r'G:\Documents\Drexel\Final_Project\EIH\iran_201901_1_tweets_csv_hashed\iran_processed.csv',
	r'G:\Documents\Drexel\Final_Project\cresci-2017.csv\datasets_full.csv\SS2_processed.csv',
	#r'G:\Documents\Drexel\Final_Project\cresci-2017.csv\datasets_full.csv\SS3_processed.csv',
	r'G:\Documents\Drexel\Final_Project\EIH\ira_processed.csv',
	#r'G:\Documents\Drexel\Final_Project\EIH\china3_processed.csv',
	r'G:\Documents\Drexel\Final_Project\cresci_2015_dataset\TFP\TFP_processed.csv',
	r'G:\Documents\Drexel\Final_Project\cresci_2015_dataset\E13\E13_processed.csv'

]

# Label of each dataset
dataset_legend = [
	0, 1, 1, 0, 0
]

# Number of rows to import from each dataset
dataset_nrows = [
	100000, 150000, 150000, 100000, 100000
]

def main():

	for i in range(len(dataset_list)):
		file_len = len(pd.read_csv(dataset_list[i], usecols=["userid"]))

		sample_size = dataset_nrows[i]

		# Adapted from https://stackoverflow.com/a/22259008
		skip = sorted(random.sample(range(1, file_len), file_len - sample_size))
		data = pd.read_csv(dataset_list[i], skiprows=skip, usecols=cols)

		# Sort columns
		data = data.reindex(sorted(data.columns), axis=1)

		# Create labels
		labels = np.full(len(data), fill_value=dataset_legend[i])

		data["bot"] = labels

		if i == 0:
			header = True
		else:
			header = False



		with open(processed_file, 'a', encoding='utf-8', newline='') as f:
			data.to_csv(f, header=header, index=False, encoding='utf-8')

		print("processed" + dataset_list[i])

	file_len = len(
		pd.read_csv(processed_file, usecols=["userid"])) + 1
	print("Num. Tweets in processed file: %d" % file_len)

if __name__ == "__main__":
	main()