import pandas as pd
import numpy as np
from keras.models import load_model

from Model import Model
from text_preprocessor import process_text


class LSTMModel(Model):
	def __init__(self, model, columns):
		super(LSTMModel, self).__init__(model, columns)
		self.vocab_size = 20000
		self.max_len = 50

	def get_probabilities(self, tweet_data: np.ndarray) -> np.ndarray:
		model = load_model(self.model)
		probs = model.predict(tweet_data)

		return probs

	def standardize(self, tweet_data: np.ndarray) -> np.ndarray:
		"""
		No standardization required with this LSTM network
		"""
		return tweet_data

	def preprocess(self, tweet_data: pd.DataFrame) -> np.ndarray:
		encoded_tweets = process_text(tweet_data, self.vocab_size, self.max_len)

		return encoded_tweets


