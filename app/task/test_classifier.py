from app.modules.modules import FilterTweetWords
from app.modules.modules import FeatureListExtractor
from app.location import AbsolutePath

import pickle
import nltk
import csv
from tabulate import tabulate
from svmutil import *
import time

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
            t1 = time.time()
            allTweetsSentiments = csv.reader(open(test_tweet_file, 'rb'), delimiter = '|')
            table_header = ['Tweet', 'Predicted_ Sentiment', 'Actual Sentiment']
            table_data = []
            for rows in allTweetsSentiments:
                tweet = rows[1]
                processedTweet = self.filterTweet.processTweet(tweet)
                featureVector = self.filterTweet.getFeatureVector(processedTweet)
                extractedFeature = self.extractor.extractFeatures(featureVector)
                table_data.append((tweet, str(self.classifier.classify(extractedFeature)), rows[0]))
            testing_data = self.extractor.NVBTrainingSetExtractor(test_tweet_file)

            t2 = time.time()
            time_taken = t2-t1
            time_minute, time_second = time_taken // 60, time_taken % 60

            print '\nNaive Bayes Classification Result:'
            print('Accuracy = ' + str(nltk.classify.accuracy(self.classifier, testing_data) * 100) + '%\nTime taken: '+str(time_minute)+' mins '+str(time_second)+' secs\n\n' )
            print tabulate(table_data, table_header)

        def SVMTestFile(self, test_tweet_file):
            t1 = time.time()
            allTweetsSentiments = csv.reader(open(test_tweet_file, 'rb'), delimiter = '|')
            table_header = ['Tweet', 'Predicted_ Sentiment', 'Actual Sentiment']
            table_data = []
            rows_count = 0.0000
            correct_prediction = 0.0000
            for rows in allTweetsSentiments:
                tweet = rows[1]
                Actual_Sentiment = rows[0]
                Predicted_Sentiment, positive_probability, negative_probability, keywords = self.SVMSingleTweet(tweet)
                table_data.append((tweet, Predicted_Sentiment, Actual_Sentiment))
                rows_count = rows_count + 1
                if Predicted_Sentiment == Actual_Sentiment:
                    correct_prediction = correct_prediction + 1

            t2 = time.time()
            time_taken = t2-t1
            time_minute, time_second = time_taken // 60, time_taken % 60

            print '\nSVM Classification Result:'
            accuracy = float(correct_prediction/rows_count) * 100
            print('Accuracy = ' + str(accuracy) + '%\nTime taken: '+str(time_minute)+' mins '+str(time_second)+' secs\n\n')
            print tabulate(table_data, table_header)


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

            p_labels, p_accs, p_vals = svm_predict([0] * len(feature_vector_test), feature_vector_test, self.svmModel, options='-q -b 1')

            for probs in p_vals:
                positive_probability = str(probs[0])
                negative_probability = str(probs[1])
            if p_labels[0] == 0.0:
                sentiment = 'negative'
            elif p_labels[0] == 1.0:
                sentiment = 'positive'
            return sentiment, positive_probability, negative_probability, keywords

    except Exception as e:
        print(e)

# x = test_classifier()
# x.NVBTestFile('./../data_files/testing_file.csv')
# x.SVMTestFile('./../data_files/testing_file.csv')