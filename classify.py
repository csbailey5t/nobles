import pandas as pd

from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer('english')
stopset = set(stopwords.words('english'))


# Read in the data
tweets = pd.read_csv('AshleyBillasanoTweets.csv', encoding='latin-1')


def tokenizer(tweet, stopset):
    # tokenize
    tokens = word_tokenize(tweet.lower())

    # remove stopwords
    tokens = [token for token in tokens if token not in stopset]
    words = [
        stemmer.stem(word)
        for word in tokens
        if word.isalnum()
    ]
    return words


def main():
    tokenTweet = tokenizer(tweets['Tweet'][0], stopset)
    print(tokenTweet)

if __name__ == '__main__':
    main()
