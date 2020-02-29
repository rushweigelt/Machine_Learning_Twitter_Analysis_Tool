'''
Rush Weigelt
Feb 2020
This script is to create Django objects out of our ML models
Lots of helper functions
'''

#Django imports
from django.db import models
#ML imports
from sklearn.naive_bayes import GaussianNB, BernoulliNB
from sklearn.model_selection import cross_validate, train_test_split, KFold
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from sklearn import metrics
from pymongo import MongoClient
import numpy as np
from joblib import load
from tensorflow.python.keras.initializers import glorot_uniform
from tensorflow.python.keras.models import load_model, model_from_json
#from tensorflow.python.keras.models import load_model, model_from_json
from keras.utils import CustomObjectScope
import re
import nltk
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from .data_manipulation import *
from .twitter_scrape import get_all_tweets

'''PART II: LOAD MODEL HELPER FUNCTIONS'''
#helper function to load a model (mfn = Model File Name)
def LoadModel(mfn):
    if mfn == 'gaussianNB':
        model = load('tat/mlModels/gaussianNB.joblib')
    elif mfn == 'LSTMText':
        model = load('tat/mlModels/LSTMModel.joblib')
    elif mfn == 'RandomForestModel':
        model = load('tat/mlModels/RandomForestModel.joblib')
    return model

def GaussianNB(hashtag):
    m = LoadModel('gaussianNB')
    print(hashtag)
    x = get_all_tweets(hashtag)
    print(x)
    predictions = m.predict(x)
    print(predictions)
    # Light number crunching for report
    bot_num = np.sum(predictions == 'bot')
    percent = bot_num / len(predictions) * 100
    statement = "For the hashtag {}: \n Out of {} analyzed tweets, {} are suspected bots. That is {}%!".format( hashtag, len(predictions), bot_num,
                                                                                        round(percent, 2))
    print(statement)
    return statement

def RandomForest(hashtag):
    m = LoadModel('RandomForestModel')
    print(hashtag)
    x, y = get_all_tweets(hashtag)
    print(x)
    predictions = m.predict(x)
    print(predictions)
    # Light number crunching for report
    bot_num = np.sum(predictions == 'bot')
    percent = bot_num / len(predictions) * 100
    statement = "For the hashtag {}: \n Out of {} analyzed tweets, {} are suspected bots. That is {}%!".format( hashtag, len(predictions), bot_num,
                                                                                        round(percent, 2))
    print(statement)
    return statement, y

#Function for our LSTM Textual Classifier
def LSTMTextClassifier(db, collect):
    #Load requested data from database
    data = read_mongo_data(db, collect)
    data = clean_twitter_data_text_analysis(data)
    #load model and weights, then open them and predict on new data
    #Utilizes a JSON object for the model and a .h5 file for the weights
    model = 'tat/mlModels/LSTMModel.json'
    weights = 'tat/mlModels/LSTMweights.h5'
    with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
        with open(model, 'r') as f:
            model = model_from_json(f.read())
        model.load_weights(weights)
    #Make predictions of new data in model
    preds = model.predict_classes(data, verbose=2)
    probs = model.predict_proba(data, verbose=2)
    #Convert to arrays, then lists. Replace numeric labels with textual for printing
    preds_arry = np.array(preds)
    probs_arry = np.array(probs)
    # Bots = 0, Genuine = 1
    combined = pd.DataFrame(np.hstack((preds_arry,probs_arry)))
    preds_lst = combined[0].tolist()
    probs_lst =  combined[1].tolist()
    #bots = 0, genuine = 1
    for x in preds_lst:
        if x ==1.0:
            preds_lst[preds_lst.index(x)] = 'genuine'
        else:
            preds_lst[preds_lst.index(x)] ='bot'
    i = 0
    '''
    for x in preds_lst:
        print("Prediction: {}       Probability: {}".format(x, probs_lst[i]))
        i + 1
    '''
    #Light number cruching for basic report
    bot_num = preds_lst.count('bot')
    percent = bot_num/len(preds_lst)*100
    statement = "Out of {} analyzed tweets, {} are suspected bots. That is {}%!".format(len(preds_lst), bot_num, round(percent, 2))
    print(statement)
    return statement
