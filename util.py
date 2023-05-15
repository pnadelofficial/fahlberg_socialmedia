import streamlit as st
from string import punctuation, digits
import collections
import re

@st.cache_data
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

def whitespace_tokenize(text):
    return [x.lower() for x in re.split(r"([.,!?]+)?\s+", text) if x]

def count_words(df, relative=False):
    word_count = collections.defaultdict(int)
    
    tokenized_tweets = df['text'].apply(whitespace_tokenize).to_list()

    es_stops = open('spanish.txt').readlines()
    es_stops = [s.strip() for s in es_stops]
    en_stops = open('english.txt').readlines()
    en_stops = [s.strip() for s in en_stops]
    all_stops = [d for d in digits] + [p for p in punctuation] + es_stops + en_stops + ['rt', '\n', '\n\n', '…', '¡', '¿', '“', '”', '...', ' ', '', '🏼', '[empty]'] 

    for tweet in tokenized_tweets:
        for word in tweet:
            if (word.lower() not in all_stops) and (word != ''):
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1 
    
    freq = sorted(word_count.items(), key=lambda x:x[1], reverse=True)
    if relative:
        freq = [(f[0], f[1]/len(freq)) for f in freq]

    return freq