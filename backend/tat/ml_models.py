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
import sys
import os
#Add another path so we do not depend on relative imports
sys.path.insert(2,os.path.dirname(os.path.abspath(__file__)))
from data_manipulation import *
from twitter_scrape import get_all_tweets, get_twitter_data_lstm
import requests
from heat_map import create_heatmap

#Certainty threshold variables for each model
randomforest_threshold_val = .68
ada_boost_threshold_val = .51
nb_threshold_val = .7

'''PART II: LOAD MODEL HELPER FUNCTIONS'''
#helper function to load a model (mfn = Model File Name)
def LoadModel(mfn):
    if mfn == 'gaussianNB':
        model = load('tat/mlModels/gaussianNB.joblib')
    elif mfn == 'LSTMText':
        model = load('tat/mlModels/LSTMModel.joblib')
    elif mfn == 'RandomForestModel':
        model = load('tat/mlModels/RandomForestModel.joblib')
    elif mfn == 'ADA':
        model = load('tat/mlModels/ADA_Model.joblib')
    return model

#Helper function to simplify calling and running our basic SKLearn models
def basicSKLearnModel(model, hashtag, threshold_val, map_bool):
    print(hashtag)
    #returned from our tweter scrape, we get the data to analyse, the data to reconstruct suspected tweets, and location data of bots
    data, reconstruct, verified_loc = get_all_tweets(hashtag)
    # print(data)
    # predictions = m.predict(data)
    certainties = model.predict_proba(data)
    predictions = []
    # create a threshold to limit false positives
    # c = certainties.tolist()
    for certainty in certainties:
        if certainty[1] >= threshold_val:
            pred = 1
        else:
            pred = 0
        predictions.append(pred)

    #print("prediction array:")
    #print(predictions)
    #print("certainties")
    #print(certainties)
    # get list of indexes of bots, to reconstruct and embed their tweets on page
    i = 0
    bots = []
    embed = []
    locs = []
    bot_sum = 0
    for prediction in predictions:
        #Check to ensure we're not calling verified accounts bots, as it is very unlikely
        if prediction == 1 and verified_loc[i][0] == False:
            #add to bot list and bot sum
            idx = i
            bot_sum += 1
            bots.append(idx)
            #Recreates the needed url to embed offending tweets
            tweet_request = requests.get(
                "https://publish.twitter.com/oembed?url=https://twitter.com/" + reconstruct[i][0] + "/status/" +
                reconstruct[i][1] + "&omit_script=true")
            tweet_json = tweet_request.json()
            tweet_html = tweet_json['html']
            embed.append(tweet_html)
            #Create heatmap
            if verified_loc[i][1] != None and verified_loc[i][1] != '':
                locs.append(verified_loc[i][1])
        i += 1
    # print(embed)
    # print("Bot indexes on main list:")
    # print(bots)
    # Light number crunching for report
    # bot_num = sum(predictions == 1)
    percent = bot_sum / len(predictions) * 100
    statement = "For the hashtag {}: \n Out of {} analyzed tweets, {} are suspected bots. That is {}%!" \
                "".format(hashtag, len(predictions), bot_sum, round(percent,2))
    #print("locations:")
    #print(locs)
    #Heatmap
    if map_bool != None:
        map = create_heatmap(locs)
    else:
        map = ''
    print(statement)
    # Returns the statistics and the tweets to embed
    return statement, embed, map


#Gaussian Naive Bayes
def GaussianNB(hashtag, map_bool):
    m = LoadModel('gaussianNB')
    return basicSKLearnModel(m, hashtag, nb_threshold_val, map_bool)
#Random Forest
def RandomForest(hashtag, map_bool):
    m = LoadModel('RandomForestModel')
    return basicSKLearnModel(m, hashtag, randomforest_threshold_val, map_bool)
#Ada Boost
def ADA(hashtag, map_bool):
    m = LoadModel('ADA')
    return basicSKLearnModel(m, hashtag, ada_boost_threshold_val, map_bool)

#Function for our LSTM Textual Classifier
def LSTMTextClassifier(hashtag, map_bool):
    #Load requested data from database
    data, reconstruct, ver_loc = get_twitter_data_lstm(hashtag)
    data = pd.DataFrame(data)
    print(data)
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
    bots = []
    i = 0
    embed = []
    locs = []
    #bots = 0, genuine = 1
    for x in preds_lst:
        if x ==1.0:
            preds_lst[preds_lst.index(x)] = 'genuine'
        elif x==0.0 and ver_loc[i][0] == False:
            preds_lst[preds_lst.index(x)] ='bot'
            tweet_request = requests.get(
                "https://publish.twitter.com/oembed?url=https://twitter.com/" + reconstruct[i][0] + "/status/" +
                reconstruct[i][1] + "&omit_script=true")
            tweet_json = tweet_request.json()
            tweet_html = tweet_json['html']
            embed.append(tweet_html)
            # Create heatmap
            if ver_loc[i][1] != None and ver_loc[i][1] != '':
                locs.append(ver_loc[i][1])
        i += 1
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
    if map_bool != None:
        map = create_heatmap(locs)
    else:
        map = ''
    return statement, embed, map




