"""keras_lstm to look at textual analysis of fake news

By Rush Weigelt
10/31/19
"""


from matplotlib import pyplot
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras import regularizers
from keras.callbacks import CSVLogger
from keras.optimizers import adam
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers.embeddings import Embedding
import numpy as np
import pandas as pd
from pathlib import Path
from nltk.corpus import stopwords
import nltk
import re
import os



#Parameters
learning_rate = .001
l2 = .1
epochs = 500
batch_size = 50
timesteps = 100
stride = 10
num_features = 3
num_hidden = 32
num_classes = 2
dropout = .5
optimizer = adam(lr=learning_rate)
parentDirectory = os.path.abspath(os.path.join(os.getcwd(), "../../../"))
data_folder = os.path.join(parentDirectory, "data")
filename = "combined_multi_bot_and_genuine_800.0k_split.csv"
data_path = os.path.join(data_folder, filename)
log_folder = os.path.join(data_folder, "lstmLog")
graph_folder = os.path.join(log_folder, "graphs")
report_filename = filename[:-4]+".log"

df = pd.read_csv(data_path, encoding='latin-1', names=['text', 'description', 'label'], error_bad_lines=False)
df = df.dropna()
df = df.applymap(str)
labels = df['label'].map(lambda x : 1 if x=='bot' else 0)
df = df[df.text.apply(lambda x: x!="")]
df = df[df.description.apply(lambda x: x !="")]
#print(df.describe())
#print(df.head)
##TAKEN FROM @sabbar
def clean_text(text):
    #Convert words to lower case and split them
    text = text.lower().split()
    #Remove stop words
    #stops = set(stopwords.words("english"))
    text = " ".join(text)
    text = re.sub(r"[^A-Za-z0-9^,!.\/'+-=]", " ", text)
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r",", " ", text)
    text = re.sub(r"\.", " ", text)
    text = re.sub(r"!", " ! ", text)
    text = re.sub(r"\/", " ", text)
    text = re.sub(r"\^", " ^ ", text)
    text = re.sub(r"\+", " + ", text)
    text = re.sub(r"\-", " - ", text)
    text = re.sub(r"\=", " = ", text)
    text = re.sub(r"'", " ", text)
    text = re.sub(r"(\d+)(k)", r"\g<1>000", text)
    text = re.sub(r":", " : ", text)
    text = re.sub(r" e g ", " eg ", text)
    text = re.sub(r" b g ", " bg ", text)
    text = re.sub(r" u s ", " american ", text)
    text = re.sub(r"\0s", "0", text)
    text = re.sub(r" 9 11 ", "911", text)
    text = re.sub(r"e - mail", "email", text)
    text = re.sub(r"j k", "jk", text)
    text = re.sub(r"\s{2,}", " ", text)
    ## Stemming
    text = text.split()
    stemmer = nltk.SnowballStemmer('english')
    stemmed_words = [stemmer.stem(word) for word in text]
    text = " ".join(stemmed_words)
    return text
##end taken from @sabbar
#apply clean text to our tweet data
df['text'] = df['text'].map(lambda x: clean_text(x))
#limit vocab size, then tokenize as a preprocessing step
vocab_size = 20000
tokenizer = Tokenizer(num_words=vocab_size)
tokenizer.fit_on_texts(df['text'])
sequences = tokenizer.texts_to_sequences(df['text'])
data = pad_sequences(sequences, maxlen=50)

#create model, add layers, compile, and fit
model_lstm = Sequential()
model_lstm.add(Embedding(vocab_size, 100, input_length=50))
model_lstm.add(LSTM(100, dropout=.2, recurrent_dropout=.2))
model_lstm.add(Dense(1, activation='sigmoid'))
model_lstm.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
train_log = os.path.join(log_folder, report_filename)
csv_logger = CSVLogger(train_log, append=False)
metrics = model_lstm.fit(data, np.array(labels), verbose=1, validation_split=.4, epochs=5, callbacks=[csv_logger])

#post fit stats
#scores = model_lstm.evaluate()

#post fit stats
word_embds = model_lstm.layers[0].get_weights()


# plot training stats
pyplot.plot(metrics.history['accuracy'], label='train')
pyplot.plot(metrics.history['val_accuracy'], label='test')
pyplot.legend()
pyplot.show()
'''
###Model###
model = Sequential()

#set it up with our vars
model.add(LSTM(num_hidden, input_shape=(timesteps, num_features), kernel_regularizer=regularizers.l2(l2)))
model.add(Dropout(dropout))

#Dense output layer
model.add(Dense(num_classes, activation='softmax'))

optimizer = adam(lr=learning_rate)
model.compile(optimizer= 'adam', loss='categorical_crossentropy',  metrics=['accuracy'])

#csv_logger = CSVLogger('training.log', append=False)

#fit the model and record training metrics

#metrics = model.fit(my_data.values, epochs=epochs, validation_split=.3)

# plot training stats
#pyplot.plot(metrics.history['acc'], label='train')
#pyplot.plot(metrics.history['val_acc'], label='test')
pyplot.legend()
pyplot.show()
'''


