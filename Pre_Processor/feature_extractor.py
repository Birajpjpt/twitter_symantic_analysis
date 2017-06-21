import re
import nltk
import csv
from filterTweetWords import Filter_Tweet_Words
from tweetProcessor import Preprocessor

class FeatureListExtractor:

    def __init__(self):
        self.filterTweetWords = Filter_Tweet_Words()
        self.processor = Preprocessor()
        self.featureList = []

    def extractFeatures(self, tweet):
        tweet_words = set(tweet)
        features = {}
        if not self.featureList:
            self.trainingSetExtractor('featureList', '../twitter_training.csv')
        for word in self.featureList:
            features['contains(%s)' % word] = (word in tweet_words)
        return features

    def trainingSetExtractor(self, task, csvFile):
        allTweetsSentiments = csv.reader(open(csvFile, 'rb'), delimiter=',')
        stopWords = self.filterTweetWords.stopWordsList()
        tweets = []
        for row in allTweetsSentiments:
            sentiment = row[0]
            tweet = row[1]
            processedTweet = self.processor.processTweet(tweet)
            featureVector = self.filterTweetWords.getFeatureVector(processedTweet)
            self.featureList.extend(featureVector)
            tweets.append((featureVector, sentiment));

        self.featureList = list(set(self.featureList))
        if task == 'featureList':
            return self.featureList
        elif task == 'train':
            training_set = nltk.classify.util.apply_features(self.extractFeatures, tweets)
            return training_set



