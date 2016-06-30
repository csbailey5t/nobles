from nltk import word_tokenize
# from nltk.corpus import stopwords

import pandas as pd

dataFile = 'AshleyBillasanoTweets.csv'
# stopset = set(stopwords.words('english'))
stopset = {'this', 'fuckked'}


def build_corpus_from_csv(filename):
    data = pd.read_csv(filename, encoding='latin-1', index_col=0)

    return data


def tokenize(text):
    tokens = [token for token
              in word_tokenize(text.lower())
              if token.isalnum()]

    return tokens


def tokenize_corpus(texts):
    return [tokenize(text) for text in texts]


def remove_stopwords(text, stopset):
    tokens = [token for token in text if token not in stopset]
    return tokens


def remove_stopwords_from_corpus(texts, stopset):
    return [remove_stopwords(text, stopset) for text in texts]


def main():
    data = build_corpus_from_csv(dataFile)
    data['Tweet'] = tokenize_corpus(data['Tweet'])
    data['Tweet'] = remove_stopwords_from_corpus(data['Tweet'], stopset)
    print(data)
    print(stopset)


if __name__ == '__main__':
    main()
