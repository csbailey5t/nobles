import spacy
import tfidf

dataFile = 'AshleyBillasanoTweets.csv'

nlp = spacy.English()


def main():

    tweets = tfidf.build_corpus_from_csv(dataFile)
    # create just a list of tweets
    tweets_only = [tweet for tweet in tweets['Tweet']]
    # loop over the tweets and print out each token and its part of speech
    for tweet in tweets_only:
        doc = nlp(u'%s' % tweet)
        for token in doc:
            print(token, token.pos, token.pos_)

if __name__ == '__main__':
    main()
