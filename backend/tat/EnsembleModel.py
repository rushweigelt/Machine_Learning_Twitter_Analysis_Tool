import pandas as pd
import numpy as np
import joblib

from Model import Model
from RFModel import RFModel
from LSTMModel import LSTMModel


class EnsembleModel(Model):
	def __init__(self, models, columns):
		super(EnsembleModel, self).__init__(None, columns)
		self.model_list = models
		self.threshold = 0.5
		self.vote_type = "AVG"

	def predict_proba(self, tweet_data: pd.DataFrame) -> np.ndarray:
		model_probs = None
		for model in self.model_list:
			predictions = model.predict_proba(tweet_data.copy())

			if model_probs is None:
				model_probs = predictions.reshape((len(predictions), 1))
			else:
				model_probs = np.append(model_probs, predictions.reshape((len(predictions), 1)), axis=1)

		if self.vote_type == "AVG":
			predictions = self.average_vote(model_probs)
		else:
			predictions = self.majority_vote(model_probs)

		return predictions

	def get_probabilities(self, X):
		pass

	def standardize(self, X):
		pass

	def preprocess(self, X):
		pass

	def majority_vote(self, probabilities: np.ndarray) -> np.ndarray:
		num_voters = probabilities.shape[1]

		for i in range(num_voters):
			probabilities[probabilities[:, i] >= self.threshold] = 1.0
			probabilities[probabilities[:, i] < self.threshold] = 0.0

		bot_votes = np.sum(probabilities, axis=0)
		human_votes = np.full(len(probabilities), fill_value=num_voters) - bot_votes

		votes = np.zeros((len(probabilities), 2))
		votes[:, 0] = human_votes
		votes[:, 1] = bot_votes

		final_votes = np.argmax(votes, axis=1)

		return final_votes

	@staticmethod
	def average_vote(probabilities: np.ndarray) -> np.ndarray:
		return np.mean(probabilities, axis=1)


if __name__ == "__main__":
	cols = ['followerscount','friendscount','replycount','likecount','retweetcount',
				'hashtagcount','mentioncount','urlcount',
				'accountrep', 'friends_growthrate', 'followers_growthrate']

	model_files = [
		r"C:\Users\Aleksi\PycharmProjects\TweetEnsemble\Models\RF_CH_V_H\RF_fold-0.joblib",
		r"C:\Users\Aleksi\PycharmProjects\TweetEnsemble\Models\RF_T_V_H\RF_fold-0.joblib",
		r"C:\Users\Aleksi\PycharmProjects\TweetEnsemble\Models\RF_MS_V_MH\RF_fold-0.joblib",
	]

	lstm_model_obj = LSTMModel("./mlModels/LSTM_model.h5", cols + ['text'])

	models = []

	for file in model_files:
		sk_model = joblib.load(file)

		model_obj = RFModel(sk_model, cols)
		models.append(model_obj)

	models.append(lstm_model_obj)

	ensemble = EnsembleModel(models, cols)
	ensemble.save_model("LSTM_ensemble_model.joblib")
