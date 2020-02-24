import matplotlib.pyplot as plt
import sys
import csv
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.utils import shuffle
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, plot_confusion_matrix, recall_score, precision_score
from sklearn.naive_bayes import GaussianNB
from sklearn_porter import Porter
import numpy as np
import pandas as pd
import k_folds as kf
import feature_engineering

DATA_PATH = r'G:\Documents\Drexel\Final_Project\russia_spam_v_multihumans_600k.csv'

DATA_COLS = ['userid', 'followerscount','friendscount','replycount','likecount','retweetcount',
			 'hashtagcount','mentioncount','urlcount','bot', 'account_createdat', 'tweet_createdat']

TRAIN_COLS = ['followerscount','friendscount','replycount','likecount','retweetcount',
				'hashtagcount','mentioncount','urlcount',
				'accountrep', 'friends_growthrate', 'followers_growthrate']

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


def get_test_train_sets(train_user_ids, test_user_ids, dataset):
	"""
	Function for retrieving data for a list of train & test user ids from data set
	"""

	# Extract records based on user id
	train_set = dataset.loc[dataset['userid'].isin(train_user_ids)]
	test_set = dataset.loc[dataset['userid'].isin(test_user_ids)]

	# Extract features to be included in training
	train_x = train_set[TRAIN_COLS].copy()
	train_y = train_set['bot'].copy()
	test_x = test_set[TRAIN_COLS].copy()
	test_y = test_set['bot'].copy()

	print("Training on: ", train_x.columns.values)

	train_x = train_x.values
	train_y = train_y.values
	test_x = test_x.values
	test_y = test_y.values

	# Remove NaN entries
	train_x = np.nan_to_num(train_x)
	test_x = np.nan_to_num(test_x)

	# print(np.count_nonzero(np.isnan(train_x)))

	# Shuffle data
	train_x, train_y = shuffle(train_x, train_y)
	test_x, test_y = shuffle(test_x, test_y)

	train_y = np.reshape(train_y, (-1, 1))
	test_y = np.reshape(test_y, (-1, 1))

	return train_x, test_x, train_y, test_y


def train_model(dataset, num_folds, standardize=False, save_model=False, m_type="RF"):
	user_ids = dataset['userid'].values
	labels = dataset['bot'].values

	# Get num_folds sets of user ids
	train_folds, test_folds = kf.get_stratified_k_folds(user_ids, labels, num_folds)

	# Train models for each CV fold
	scores = []
	for i in range(num_folds):
		if m_type == "RF":
			model = RandomForestClassifier(n_estimators=100, criterion='gini', verbose=1, max_depth=20)
		elif m_type == "ADA":
			model = AdaBoostClassifier()
		elif m_type == "KNN":
			model = KNeighborsClassifier()
		elif m_type == "MLP":
			model = MLPClassifier((32, 32), solver='adam', verbose=1, max_iter=50)
		elif m_type == "GNB":
			model = GaussianNB()
		else:
			print("Unknown model type.")
			sys.exit(-1)

		# Create train and test sets based on the user id splits
		train_x, test_x, train_y, test_y = get_test_train_sets(train_folds[i], test_folds[i], dataset)

		print("Train records: ", len(train_x))
		print("Test records: ", len(test_x))

		dist = get_class_dist(train_y, test_y)
		print("Train Fold %d class distribution: %.2f bots, %.2f humans" % (i, dist[0], dist[1]))
		print("Test Fold %d class distribution: %.2f bots, %.2f humans" % (i, dist[2], dist[3]))

		if standardize:
			scaler = StandardScaler()
			scaler.fit(train_x)
			train_x = scaler.transform(train_x, copy=True)
			test_x = scaler.transform(test_x, copy=True)

			# Save the standardization info
			np.savetxt(m_type + "means_fold-" + str(i) + ".csv", scaler.mean_, delimiter=",")
			np.savetxt(m_type + "scale_fold-" + str(i) + ".csv", scaler.var_, delimiter=",")

		# Train the model
		model.fit(train_x, train_y.flatten())

		# Get predictions
		predicted_y = model.predict(test_x)

		# Evaluate
		score = round(accuracy_score(test_y.flatten(), predicted_y), 3)
		recall = round(recall_score(test_y.flatten(), predicted_y), 3)
		precision = round(precision_score(test_y.flatten(), predicted_y), 3)
		print(f"Accuracy score: {score}")

		# Plot & save CM
		cm_plot = plot_confusion_matrix(model, test_x, test_y, cmap=plt.cm.Blues, normalize='true')
		cm_plot.ax_.set_title(("Fold-%d" % i))
		plt.savefig(m_type + "_fold-" + str(i) + "_Acc-" + str(int(10000*score)) + ".png")

		# Export model to file
		if save_model:
			porter = Porter(model, language='js')
			output = porter.export()
			model_file = open(m_type + "_fold-" + str(i) + ".js",'w')
			model_file.write(output)

		model_result = {"Fold": i, "Accuracy": score,"Recall": recall,"Precision": precision,
						"N Train":len(train_y), "N Test": len(test_y), "Train Bot dist": dist[0],
						"Train Human dist": dist[1], "Test Bot dist": dist[2], "Test Human dist": dist[3]}

		scores.append(model_result)

	return scores


def load_dataset(data_dir):
	"""
	Function for constructing the data set
	"""
	dataset = pd.read_csv(data_dir, usecols=DATA_COLS, dtype=DTYPES)

	dataset = add_features(dataset)

	return dataset


def add_features(dataset):
	"""
	Function for adding engineered features to data set
	"""

	account_rep = feature_engineering.friends_followers_ratio(dataset["friendscount"].values,
														  dataset["followerscount"].values)

	acc_age = feature_engineering.account_age(dataset["account_createdat"].values,dataset["tweet_createdat"].values)

	friends_growth = feature_engineering.growth_rate(dataset["friendscount"].values, acc_age)

	followers_growth = feature_engineering.growth_rate(dataset["followerscount"].values, acc_age)

	dataset["accountrep"] = account_rep
	dataset["followers_growthrate"] = followers_growth
	dataset["friends_growthrate"] = friends_growth

	return dataset


def get_class_dist(train_y, test_y):
	"""
	Function for getting the train & test set class distributions
	"""
	train_bot_dist = round(len(train_y[train_y == 1]) / len(train_y), 2)
	train_hum_dist = round(len(train_y[train_y == 0]) / len(train_y), 2)

	test_bot_dist = round(len(test_y[test_y == 1]) / len(test_y), 2)
	test_hum_dist = round(len(test_y[test_y == 0]) / len(test_y), 2)

	return [train_bot_dist, train_hum_dist, test_bot_dist, test_hum_dist]


def make_report(results):
	"""
	Function for writing training results to a csv file
	"""
	cols = list(dict.keys(results[0]))

	# Dict to CSV code adapted from:
	# https://www.tutorialspoint.com/How-to-save-a-Python-Dictionary-to-CSV-file
	with open("results.csv", "w", newline='') as file:
		writer = csv.DictWriter(file, fieldnames=cols)
		writer.writeheader()

		for result in results:
			writer.writerow(result)


def main():
	np.random.seed(0)

	dataset = load_dataset(DATA_PATH)

	scores = train_model(dataset, 3, m_type="RF", standardize=False)

	for i in range(len(scores)):
		print("Test fold", i, "score:", scores[i])

	make_report(scores)


if __name__ == "__main__":
	main()
