# import svm
# from svmutil import *
#
# #training data
# labels = [0, 1, 1, 2]
# samples = [[1, 0], [1, 1], [1, 0], [0, 0]]
#
# #SVM params
# param = svm_parameter()
# param.C = 10
# param.kernel_type = LINEAR
# #instantiate the problem
# problem = svm_problem(labels, samples)
# #train the model
# model = svm_train(problem, param)
# # saved model can be loaded as below
# #model = svm_load_model('model_file')
#
# #save the model
# # svm_save_model('model_file', model)
#
# #test data
# test_data = [[1, 1], [0, 1]]
# #predict the labels
# p_labels, p_accs, p_vals = svm_predict([0]*len(test_data), test_data, model)
# print p_labels

import svm
from svmutil import *

from Algorithm.SVM_Classifier import SVM_Classifier
from Pre_Processor.feature_extractor import FeatureListExtractor
from Pre_Processor.filterTweetWords import Filter_Tweet_Words
from Pre_Processor.tweetProcessor import Preprocessor
import csv



def getSVMFeatureVector(tweets):
    processor = Preprocessor()
    tweets_sentiments = csv.reader(open(tweets, 'rb'), delimiter=',')
    for tweet in tweets_sentiments:
        training_tweet = tweet[1]
        training_label = tweet[0]
        training_tweet = processor.processTweet(training_tweet)
        model = svm_train(training_label, training_tweet)
        p_labels, p_accs, p_vals = svm_predict()

getSVMFeatureVector('hey yo')