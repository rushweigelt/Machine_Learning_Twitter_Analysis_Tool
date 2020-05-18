
from sklearn.metrics import accuracy_score, plot_confusion_matrix, recall_score, precision_score
import pandas as pd
import numpy as np
import joblib

from EnsembleModel import EnsembleModel
from RFModel import RFModel
from LSTMModel import LSTMModel

DATA_COLS = ['text', 'userid', 'followerscount','friendscount','replycount','likecount','retweetcount',
			 'hashtagcount','mentioncount','urlcount', 'account_createdat', 'tweet_createdat', 'bot']

TRAIN_COLS = ['followerscount','friendscount','replycount','likecount','retweetcount',
				'hashtagcount','mentioncount','urlcount']

DTYPES = {
			'userid':str,
			'account_createdat':str,
			'tweet_createdat':str,
			'retweetcount':float,
			'likecount':float,
			'followerscount':float,
			'friendscount':float,
			'replycount':float,
			'hashtagcount':float,
			'urlcount':float,
			'mentioncount':float,
			'bot':int
		  }


def evaluate():
	model_file = "./mlModels/LSTM_ensemble_model.joblib"
	ensemble_model = joblib.load(model_file)

	#dataset = pd.read_csv(r"G:\Documents\Drexel\Final_Project\trolls_v_humans_500k.csv", usecols=DATA_COLS, dtype=DTYPES)
	dataset = pd.read_csv(r"./trolls_redux.csv",
						  usecols=DATA_COLS, dtype=DTYPES)

	dataset = dataset.dropna()

	dataset = dataset.iloc[10:100, :].copy()

	test_x = dataset[DATA_COLS[:-1]]
	test_y = dataset["bot"].values.astype(int)

	test_x = RFModel.add_features(test_x)

	predicted_y = ensemble_model.predict_proba(test_x)

	# Evaluate
	score = round(accuracy_score(test_y.flatten(), np.round(predicted_y).astype(int)), 3)
	recall = round(recall_score(test_y.flatten(), np.round(predicted_y).astype(int)), 3)
	precision = round(precision_score(test_y.flatten(), np.round(predicted_y).astype(int)), 3)
	print(f"Accuracy score: {score}")
	print(f"Recall score: {recall}")
	print(f"Precision score: {precision}")


if __name__ == "__main__":
	evaluate()

