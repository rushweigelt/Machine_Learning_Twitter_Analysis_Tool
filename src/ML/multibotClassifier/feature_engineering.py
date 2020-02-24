import numpy as np
import re
from dateutil import parser


def friends_followers_ratio(friends, followers):
	"""
	Function for getting the normalized friends to followers ratio, as specified in:
	Wang, Haining. "Detecting Automation of Twitter Accounts: Are You a Human, Bot or Cyborg?"
	IEEE Transactions on Dependable and Secure Computing. November 2012.

	Args:
		friends - 1xN numpy array of friend counts
		followers - 1xN numpy array of follower counts

	Returns:
		1xN numpy array containing friends to followers ratios
	"""

	# Zero division handling adapted from DStauffman's solution at:
	# https://stackoverflow.com/a/37977222
	return np.divide(followers, (friends + followers), out=np.zeros_like(followers),
					 where=(friends + followers) != 0)


def account_age(account_createdat, tweet_createdat):
	"""
	Function for getting the account age, as specified in:
	Yang, Kai-Cheng. "Scalable and Generalizable Social Bot Detection through Data Selection"
	arXiv, November 2019

	Args:
		account_createdat - 1xN numpy array of account creation dates in string format

		tweet_createdat - 1xN numpy array of tweet creation dates in string format

	Returns:
		1xN numpy array containing the account age in hours
	"""

	# Remove timezone info
	rem_tz = np.vectorize(lambda x: re.sub(r"\s\+[0-9]{4}\s", " ", x))
	account_createdat = rem_tz(account_createdat)
	tweet_createdat = rem_tz(tweet_createdat)

	# Parse date from string
	dt_convert = np.vectorize(lambda x: parser.parse(x))

	account_createdat = dt_convert(account_createdat)
	tweet_createdat = dt_convert(tweet_createdat)

	# Find the age by taking difference of tweet and acc creation dates
	acc_age = tweet_createdat - account_createdat

	# Convert the time delta object to hours
	hours_convert = np.vectorize(lambda x: x.total_seconds() / 3600)
	acc_age = hours_convert(acc_age)

	return acc_age


def growth_rate(feature, acc_age):
	"""
		Function for getting the growth rate of a feature as specified in:
		Yang, Kai-Cheng. "Scalable and Generalizable Social Bot Detection through Data Selection"
		arXiv, November 2019

		Args:
			feature - 1xN numpy array containing numerical feature values

			account_createdat - 1xN numpy array of account creation dates in string format

			tweet_createdat - 1xN numpy array of tweet creation dates in string format

		Returns:
			1xN numpy array containing growth rate per hour of the feature
		"""

	feature_gr = np.divide(feature, acc_age)

	return feature_gr


if __name__ == "__main__":
	print(account_age(np.asarray(["11/6/2015", "7/26/2013"]),
					  np.asarray(["1/14/2017  21:29:00", "6/5/2016  03:41:00"])))
