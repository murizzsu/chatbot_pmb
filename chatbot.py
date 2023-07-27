from flask_cors import CORS
from flask import Flask
import pickle
import random
from colorama import Fore, Style
import json
import numpy as np
import pandas as pd
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
import colorama
from keras.models import load_model
from keras_preprocessing.sequence import pad_sequences
import string
import nltk
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

colorama.init()


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

import codecs
with codecs.open('jsonformatter.txt', 'r', encoding='utf-8') as file:
    data = json.load(file)

#Global Variabel
input_shape = 7
trunc_type='post'
padding_type='post'

### Dataset
# with open("jsonformatter.json") as file:
#     data = json.load(file)

key_norm = pd.read_csv('key_norm.csv')

##Stopword
nltk.download('stopwords')
stopwords_ind = stopwords.words('indonesian')
more_stopword = ['kak', 'informasi', "tentang", "terkait", "sih", "ngapain", "dipenuhi", "aja", "dah", "ya", "ummi", "izin", "guna", "kan", "gak", "gk"]
stopwords_ind = stopwords_ind + more_stopword
def remove_stop_words(text):
  clean_words = []
  text = text.split()
  for word in text:
      if word not in stopwords_ind:
          clean_words.append(word)
  return " ".join(clean_words)

### Word Normalization
def text_normalize(text):
  text = ' '.join([key_norm[key_norm['singkat'] == word]['hasil'].values[0] if (key_norm['singkat'] == word).any() else word for word in text.split()])
  text = str.lower(text)
  print(text)
  return text

### Stemming
factory = StemmerFactory()
stemmer = factory.create_stemmer()
def stemming(text):
  text = stemmer.stem(text)
  print(text)
  return text

### Implementasi Fungsi
def text_preprocessing_process(text):
  text = text_normalize(text)
  text = remove_stop_words(text)
  text = stemming(text)
  return text

def get_response(inp):
    # load trained model
    model = load_model('chat_model')

    # load tokenizer object
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    # load label encoder object
    with open('label_encoder.pickle', 'rb') as enc:
        lbl_encoder = pickle.load(enc)

    texts_p = []
    #removing punctuation
    prediction_input = [letters.lower() for letters in inp if letters not in string.punctuation]
    prediction_input = ''.join(prediction_input)
    prediction_input = text_preprocessing_process(prediction_input)
    texts_p.append(prediction_input)

    print("text_p",texts_p)
    #tokenizing and padding
    prediction_input = tokenizer.texts_to_sequences(texts_p)
    prediction_input = np.array(prediction_input).reshape(-1)
    prediction_input = pad_sequences([prediction_input],input_shape, padding=padding_type, truncating=trunc_type)
    jumlah = sum(np.array(prediction_input).reshape(-1))
    print(jumlah)
    print('prediction_input', prediction_input)
    print('jumlah', jumlah)
    output = model.predict(prediction_input)
    print(output)
    tag = LabelEncoder.inverse_transform(lbl_encoder, [np.argmax(output)])
    print(tag)
    max_prob = max(model.predict(prediction_input))
    max_idx = np.argmax(output)
    output = output.argmax()
    #finding the right tag and predicting
    
    if jumlah < 1:
        return "Maaf saya tidak mengerti"
    else:
        for i in data['intents']:
            if i['tag'] == tag:
                responseMessage = np.random.choice(i['responses'])
                print(str(i['tag']))
                if str(i['tag']) == 'bye' :
                    print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL, "Bye")
                return responseMessage

