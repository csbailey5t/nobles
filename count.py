from nltk.corpus import stopwords
from nltk.probability import FreqDist
import tfidf

dataFile = 'AshleyBillasanoTweets.csv'


def get_most_frequent_words(tokenized_corpus, num_words):
    for entry in tokenized_corpus:
        fd = FreqDist(entry)
        most_common_words = fd.most_common(num_words)
        print(most_common_words)


def main():
    tweets = tfidf.build_corpus_from_csv(dataFile, 'Tweet')

    stopset = set(stopwords.words('english'))

    tokenized_tweets = tfidf.tokenize_corpus(tweets, stopset)

    get_most_frequent_words(tokenized_tweets, 10)


if __name__ == '__main__':
    main()
