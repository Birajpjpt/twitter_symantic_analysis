from app.modules.modules import FilterTweetWords
from app.modules.modules import FeatureListExtractor
from app.location import AbsolutePath

import pickle
import nltk
import csv
from tabulate import tabulate
from svmutil import *

class test_classifier:
    try:
        def __init__(self):
            self.extractor = FeatureListExtractor()
            self.filterTweet = FilterTweetWords()
            self.location = AbsolutePath()
            self.nbClassifier = self.location.nbClassifier
            self.svmClassifier = self.location.svmClassifier

            f = open(self.nbClassifier, 'rb')
            self.classifier = pickle.load(f)
            f.close()

            self.svmModel = svm_load_model(self.svmClassifier)

        def NVBSingleTweet(self, tweet):
            testTweet = tweet
            processedTweet = self.filterTweet.processTweet(testTweet)
            featureVector = self.filterTweet.getFeatureVector(processedTweet)
            extractedFeature = self.extractor.extractFeatures(featureVector)
            return self.classifier.classify(extractedFeature), featureVector

        def NVBTestFile(self, test_tweet_file):
            allTweetsSentiments = csv.reader(open(test_tweet_file, 'rb'), delimiter = ',')
            table_header = ['Tweet', 'Sentiment']
            table_data = []
            for rows in allTweetsSentiments:
                tweet = rows[1]
                processedTweet = self.filterTweet.processTweet(tweet)
                featureVector = self.filterTweet.getFeatureVector(processedTweet)
                extractedFeature = self.extractor.extractFeatures(featureVector)
                table_data.append((tweet, str(self.classifier.classify(extractedFeature))))
            testing_data = self.extractor.NVBTrainingSetExtractor(test_tweet_file)
            print '\nNaive Bayes Classification Result:'
            print('Accuracy = ' + str(nltk.classify.accuracy(self.classifier, testing_data) * 100) + '% \n\n' )
            print tabulate(table_data, table_header)

        def SVMTestFile(self, test_tweet_file):
            test_feature_vector_and_labels = self.extractor.SVMTrainingSetExtractor(test_tweet_file)
            test_feature_vector = test_feature_vector_and_labels['feature_vector']
            print('\n\nSVM Classification Result:')
            svm_predict([0] * len(test_feature_vector), test_feature_vector, self.svmModel, options='-b 1')

        def SVMSingleTweet(self, tweet):
            map = {}
            keywords = []
            filterTweetWords = FilterTweetWords()
            feature_vector_test = []
            processedTweet = filterTweetWords.processTweet(tweet)
            featureList = self.extractor.featureList
            sortedFeature = sorted(featureList)
            featureVector = filterTweetWords.getFeatureVector(processedTweet)
            for w in sortedFeature:
                map[w] = 0
            for word in featureVector:
                if word in map:
                    map[word] = 1
                    keywords.append(word)
            values = map.values()
            feature_vector_test.append(values)

            p_labels, p_accs, p_vals = svm_predict([0] * len(feature_vector_test), feature_vector_test, self.svmModel, options='-b 1')

            for probs in p_vals:
                positive_probability = str(probs[0])
                negative_probability = str(probs[1])
            if p_labels[0] == 0.0:
                sentiment = 'Negative'
            elif p_labels[0] == 1.0:
                sentiment = 'Positive'
            return sentiment, positive_probability, negative_probability, keywords

    except Exception as e:
        print(e)