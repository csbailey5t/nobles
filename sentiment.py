from textblob import TextBlob
import tfidf

dataFile = 'AshleyBillasanoTweets.csv'


def main():

    tweets = tfidf.build_corpus_from_csv(dataFile)
    # create just a list of tweets
    tweets_only = [tweet for tweet in tweets['Tweet']]
    # loop over the tweets and print out each token and its part of speech
    for tweet in tweets_only:
        single_tweet = TextBlob(tweet)
        print(tweet)
        print(single_tweet.sentiment)

if __name__ == '__main__':
    main()
