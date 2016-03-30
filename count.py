from nltk.corpus import stopwords
from nltk.probability import FreqDist
import tfidf

dataFile = 'AshleyBillasanoTweets.csv'


def get_most_frequent_words(corpus, num_words):
    for (num, entry) in corpus.iterrows():
        fd = FreqDist(entry['Tweet'])
        most_common_words = fd.most_common(num_words)
        print(num, most_common_words)


def main():
    tweets = tfidf.build_corpus_from_csv(dataFile)

    stopset = set(stopwords.words('english'))

    tweets['Tweet'] = tfidf.tokenize_corpus(tweets['Tweet'], stopset)

    get_most_frequent_words(tweets, 10)


if __name__ == '__main__':
    main()
