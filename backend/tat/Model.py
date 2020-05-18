import abc
import pandas as pd
import numpy as np
import joblib


class Model(abc.ABC):
	def __init__(self, model, columns):
		self.model = model
		self.columns = columns

	def predict_proba(self, tweet_data: pd.DataFrame) -> np.ndarray:

		processed_td = self.preprocess(tweet_data)

		standardized_td = self.standardize(processed_td)

		predictions = self.get_probabilities(standardized_td)

		return predictions

	def save_model(self, save_path):
		joblib.dump(self, save_path)

	@abc.abstractmethod
	def get_probabilities(self, X) -> np.ndarray:
		pass

	@abc.abstractmethod
	def standardize(self, X) -> np.ndarray:
		pass

	@abc.abstractmethod
	def preprocess(self, X):
		pass








