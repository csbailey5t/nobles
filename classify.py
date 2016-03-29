import pandas as pd

from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

from sklearn.feature_extraction.text import TfidfVectorizer

stemmer = SnowballStemmer('english')
stopset = set(stopwords.words('english'))

dataFile = 'AshleyBillasanoTweets.csv'


def build_corpus_from_csv(filename, column):
    corpus = []
    data = pd.read_csv(filename, encoding='latin-1', index_col=0)
    for entry in data[column]:
        corpus.append(entry)

    return corpus


def tokenizer(tweet, stopset):
    # tokenize
    tokens = word_tokenize(tweet.lower())

    # remove stopwords
    tokens = [token for token in tokens if token not in stopset]
    words = [
        # stemmer.stem(word)
        word
        for word in tokens
        if word.isalnum()
    ]
    return words


def create_vectorizer(corpus):
    vectorizer = TfidfVectorizer(input='content', stop_words='english')
    vectorizer.fit_transform(corpus)

    return vectorizer


def get_features(corpus):
    vectorizer = create_vectorizer(corpus)
    features = vectorizer.get_feature_names()

    return features


def main():

    corpus = build_corpus_from_csv(dataFile, 'Tweet')

    tweet_feats = get_features(corpus)

    print(tweet_feats)

if __name__ == '__main__':
    main()
