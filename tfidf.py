from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer

stemmer = SnowballStemmer('english')
stopset = set(stopwords.words('english'))

dataFile = 'AshleyBillasanoTweets.csv'


def build_corpus_from_csv(filename):
    data = pd.read_csv(filename, encoding='latin-1', index_col=0)

    return data


def tokenizer(text, stopset):
    # tokenize
    tokens = word_tokenize(text.lower())

    # remove stopwords
    tokens = [token for token in tokens if token not in stopset]
    words = [
        # stemmer.stem(word)
        word
        for word in tokens
        if word.isalnum()
    ]
    return words


def tokenize_corpus(texts, stopset):
    return [tokenizer(text, stopset) for text in texts]


def create_fitted_vectorizer(corpus):
    vectorizer = TfidfVectorizer(input='content', stop_words='english')
    X = vectorizer.fit_transform(corpus)

    return X


def create_vectorizer(corpus):
    vectorizer = TfidfVectorizer(input='content', stop_words='english')
    vectorizer.fit_transform(corpus)

    return vectorizer


def get_features(corpus):
    vectorizer = create_vectorizer(corpus)
    features = vectorizer.get_feature_names()

    return features


def top_tfidf_feats(row, features, top_n=25):
    top_ids = np.argsort(row)[::-1][:top_n]
    top_features = [(features[i], row[i]) for i in top_ids]

    df = pd.DataFrame(top_features)
    df.columns = ['feature', 'tfidf']

    return df


def top_mean_feats(X, features, grp_ids=None, min_tfidf=0.1, top_n=25):
    if grp_ids:
        D = X[grp_ids].toarray()
    else:
        D = X.toarray()

    D[D < min_tfidf] = 0
    tfidf_means = np.mean(D, axis=0)

    featsDf = top_tfidf_feats(tfidf_means, features, top_n)

    return featsDf


def main():

    data = build_corpus_from_csv(dataFile)
    tweets = [tweet for tweet in data['Tweet']]

    fitted_vectorizer = create_fitted_vectorizer(tweets)
    tweet_feats = get_features(tweets)
    # print(tweet_feats)
    mean_feats = top_mean_feats(fitted_vectorizer, tweet_feats)
    print(mean_feats)

if __name__ == '__main__':
    main()
