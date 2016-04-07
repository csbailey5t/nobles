from nltk.corpus import stopwords
from nltk.probability import FreqDist
import tfidf
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer

dataFile = 'AshleyBillasanoTweets.csv'


def get_most_frequent_words(corpus, num_words):
    for (num, entry) in corpus.iterrows():
        fd = FreqDist(entry['Tweet'])
        most_common_words = fd.most_common(num_words)
        print(num, most_common_words)


def main():
    # create tweets dataframe
    tweets = tfidf.build_corpus_from_csv(dataFile)
    # create just a list of tweets
    tweets_only = [tweet for tweet in tweets['Tweet']]
    # define stopset
    stopset = set(stopwords.words('english'))
    # tokenize the tweets in place
    tweets['Tweet'] = tfidf.tokenize_corpus(tweets['Tweet'], stopset)
    # print the 10 most frequent words for each tweet
    get_most_frequent_words(tweets, 10)

    ##############################

    # create vectorizer
    vectorizer = TfidfVectorizer(input='content', stop_words=stopset)
    # fit the vectorizer
    vectorizer.fit_transform(tweets_only)
    # get feature names
    tweet_features = vectorizer.get_feature_names()

    # Generate frequency distrubutions for each tweet
    freqs = []
    indices = []
    for (num, entry) in tweets.iterrows():
        freqs.append(FreqDist(entry['Tweet']))
        indices.append(num)
    # loop over the features, and insert frequences in the dataframe
    for feature in tweet_features:
        tweets[feature] = pd.Series(
            [fd[feature] for fd in freqs],
            index=indices
        )
    # output a csv
    tweets.to_csv('frequencies.csv')


if __name__ == '__main__':
    main()
