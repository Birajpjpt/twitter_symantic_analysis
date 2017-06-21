from Pre_Processor.tweetProcessor import Preprocessor
from Pre_Processor.feature_extractor import FeatureListExtractor
from Pre_Processor.filterTweetWords import Filter_Tweet_Words
from Algorithm.SVM_Classifier import SVM_Classifier
import pickle
import nltk
import csv
from tabulate import tabulate
from svmutil import *

class run:
    def __init__(self):
        self.processor = Preprocessor()
        self.extractor = FeatureListExtractor()
        self.filterTweet = Filter_Tweet_Words()

        f = open('../NBclassifier.pickle', 'rb')
        self.classifier = pickle.load(f)
        f.close()

        self.svmClassifier = SVM_Classifier()
        self.svmModel = svm_load_model('../SVMClassifier')

    def getResult(self, tweet):
        testTweet = tweet
        processedTweet = self.processor.processTweet(testTweet)
        featureVector = self.filterTweet.getFeatureVector(processedTweet)
        extractedFeature = self.extractor.extractFeatures(featureVector)

        return self.classifier.classify(extractedFeature), featureVector

    def multiAnalysis(self, test_tweet_file):
        allTweetsSentiments = csv.reader(open(test_tweet_file, 'rb'), delimiter = ',')
        table_header = ['Tweet', 'Sentiment']
        tweet_data = []
        for rows in allTweetsSentiments:
            tweet = rows[1]
            processedTweet = self.processor.processTweet(tweet)
            featureVector = self.filterTweet.getFeatureVector(processedTweet)
            extractedFeature = self.extractor.extractFeatures(featureVector)
            tweet_data.append((tweet, str(self.classifier.classify(extractedFeature))))
        testing_data = self.extractor.trainingSetExtractor('train', test_tweet_file)
        print tabulate(tweet_data, table_header)
        print('\n \nAccuracy Percentage = ' + str(nltk.classify.accuracy(self.classifier, testing_data) * 100) + '% \n\n' )

    def SVMtestFile(self, test_tweet_file):
        print self.svmModel
        test_feature_vector_and_labels = self.svmClassifier.getSVMFeatureVector(test_tweet_file)
        test_feature_vector = test_feature_vector_and_labels['feature_vector']
        p_labels, p_accs, p_vals = svm_predict([0] * len(test_feature_vector), test_feature_vector, self.svmModel, options='-q -b 1')
        print p_labels
        print p_accs
        print p_vals

    def SVMtestSingleTweet(self, tweet):
        map = {}
        keywords = []
        filterTweetWords = Filter_Tweet_Words()
        feature_vector_test = []
        processor = Preprocessor()
        processedTweet = processor.processTweet(tweet)
        featureList = SVM_Classifier().featureList
        sortedFeature = sorted(featureList)
        print len(featureList)
        extract_feature_list = FeatureListExtractor()
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
            sentiment = 'Negative'
        elif p_labels[0] == 1.0:
            sentiment = 'Positive'
        return sentiment, positive_probability, negative_probability, str(keywords)
        # print p_vals



# x = run()
# # x.SVMtestFile('../testing_file.csv')
# x.SVMtestSingleTweet('I do not believe that my internet service provider is giving me good service. I contact them over e-mail and they never get back to me!')
# # x.multiAnalysis('../testing_file.csv')
# x.getResult('I do not believe that my internet service provider is giving me good service. I contact them over e-mail and they never get back to me!')