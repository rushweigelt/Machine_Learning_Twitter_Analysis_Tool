from Model import Model
import feature_engineering as fe
import pandas as pd
import numpy as np


class RFModel(Model):
	def __init__(self, model, columns, add_features=False):
		super(RFModel, self).__init__(model, columns)
		self.add_features = add_features

	def get_probabilities(self, tweet_data: np.ndarray) -> np.ndarray:
		probs = self.model.predict_proba(tweet_data)
		probs = probs[:, 1]

		return probs

	def standardize(self, tweet_data: np.ndarray) -> np.ndarray:
		"""
		RF model requires no standardization
		"""
		return tweet_data

	def preprocess(self, tweet_data: pd.DataFrame) -> np.ndarray:
		# Add engineered features
		if self.add_features:
			aug_tweet_data = self.add_features(tweet_data)
		else:
			aug_tweet_data = tweet_data

		# Extract columns needed
		cut_tweet_data = aug_tweet_data[self.columns].copy()

		return cut_tweet_data.values

	@staticmethod
	def add_features(tweet_data: pd.DataFrame) -> pd.DataFrame:
		"""
		Function for adding engineered features to data set
		"""

		account_rep = fe.friends_followers_ratio(tweet_data["friendscount"].values, tweet_data["followerscount"].values)

		acc_age = fe.account_age(tweet_data["account_createdat"].values, tweet_data["tweet_createdat"].values)

		friends_growth = fe.growth_rate(tweet_data["friendscount"].values, acc_age)

		followers_growth = fe.growth_rate(tweet_data["followerscount"].values, acc_age)

		tweet_data["accountrep"] = account_rep
		tweet_data["followers_growthrate"] = followers_growth
		tweet_data["friends_growthrate"] = friends_growth

		return tweet_data
