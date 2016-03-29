# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 12:14:29 2016

@author: anobles
"""
import pandas as pd
import re
from nltk import word_tokenize
from nltk.corpus import stopwords

# Set path to file
file_path = '/Users/anobles/Documents/Suicide_NLP/CaseStudy_Ashley/AshleyBillasanoTweets.csv'
# Read in csv
data = pd.read_csv(file_path, header=0)
#data = pd.read_csv('/Users/anobles/Documents/Suicide_NLP/CaseStudy_Ashley/AshleyBillasanoTweets.csv', header=0)

# Just checking out the data
data.shape
data.head()
print data["Tweet"][0]
data.columns.values

# Function to change tweets into words
def tweet_to_words(raw_data):
    # Remove non-letters
    letters_only = re.sub("[^a-zA-a]", " ", raw_data)
    # Convert to lower case
    lower=letters_only.lower()
    # Convert to tokens
    words=word_tokenize(lower)
    # Remove stopwords
    stops=set(stopwords.words("english"))
    meaningful_words = [w for w in words if not w in stops]
    return(meaningful_words)

# Try tweet_to_words function on a single tweet
test = tweet_to_words(data["Tweet"][0])
print test

# Try tweet_to_words function on all tweets
# Get total number of tweets
num_tweets = data["Tweet"].size
# Initialize an empty list to hold clean tweets
clean_tweets = []
# Loop over each tweet; create an index i that goes from 0 to the length
# of the tweets
for i in xrange(0,num_tweets):
    clean_tweets.append(tweet_to_words(data["Tweet"][i]))
    
    
# Now start with creating features with bag of words @
# https://www.kaggle.com/c/word2vec-nlp-tutorial/details/part-1-for-beginners-bag-of-words
    
    
# How can I replace the loop with an apply function?
# Can I define stops as a global variable outside of the loop for efficiency?
# Why not num_tweets-1? Thought I should only index through 143?
# What if I want to create my own stopwords list and include self-reference me?
# Do I need to put into unicode?
# Read analysis in suicide case study paper and see what I want to do next


## Playing around with sklearn
from sklearn.feature_extraction.text import CountVectorizer
counts = CountVectorizer(data.Tweet)

## Playing around with snowball stemmer from nltk
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")
stemmer.stem("hello")