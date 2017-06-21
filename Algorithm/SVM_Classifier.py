import svm
from svmutil import *
from Pre_Processor.feature_extractor import FeatureListExtractor
from Pre_Processor.filterTweetWords import Filter_Tweet_Words
from Pre_Processor.tweetProcessor import Preprocessor
import csv
import pickle
from sklearn.externals import joblib

class SVM_Classifier:
    def __init__(self):
        self.featureListExtractor = FeatureListExtractor()
        self.filterTweetWords = Filter_Tweet_Words()
        self.processor = Preprocessor()
        self.featureList = self.featureListExtractor.trainingSetExtractor('featureList', '../twitter_training.csv')
        self.training_file = '../twitter_training.csv'

    def getSVMFeatureVector(self, tweet_file):
        tweet_sentiment = csv.reader(open(tweet_file, 'rb'), delimiter=',')
        sortedFeatures = sorted(self.featureList)
        tweets = []
        for row in tweet_sentiment:
            sentiment = row[0]
            tweet = row[1]
            processedTweet = self.processor.processTweet(tweet)
            featureVector = self.filterTweetWords.getFeatureVector(processedTweet)
            tweets.append((featureVector, sentiment));
        map = {}
        feature_vector = []
        labels = []
        for t in tweets:
            label = 0
            # map = {}
            for w in sortedFeatures:
                map[w] = 0

            tweet_words = t[0]
            sentiment = t[1]

            for word in tweet_words:
                # word = self.filterTweetWords.replaceRepetitiveCharacters(words)
                # word = word.strip('\'"?,.')
                if word in map:
                    map[word] = 1

            values = map.values()
            feature_vector.append(values)
            if(sentiment == 'positive'):
                label = 1
            elif(sentiment == 'negative'):
                label = 0
            labels.append(label)

        return {'feature_vector' : feature_vector, 'labels': labels}

    def trainClassifier(self):
        result = self.getSVMFeatureVector(self.training_file)
        problem = svm_problem(result['labels'], result['feature_vector'])
        param = svm_parameter('-q -b 1')
        param.kernel_type = LINEAR
        classifier = svm_train(problem, param)
        svm_save_model('../SVMClassifier', classifier)
        print classifier
        print ('SVM Training Complete.....')



