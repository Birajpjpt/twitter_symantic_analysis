import pandas
import os
import tweepy
from tweepy import OAuthHandler
import time
import json
from elasticsearch import Elasticsearch
import requests
import sys
from app.task.test_classifier import test_classifier
import pymongo
from pymongo import MongoClient
from Twitter_Crawler import Twitter

class Analyser:
    def __init__(self):
        self.test_classifier = test_classifier()
        self.client = MongoClient('localhost', 27017)
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        self.test_classifier = test_classifier()
        self.credibility_checker = Twitter()

    def callFromDatabase(self):
        db = self.client['wannacry_db_live']
        tweets_object = db.tweets.find()
        return tweets_object

    def pushToElasticSearch(self, data_json):
        for tweet_object in data_json:
            tweet = str(tweet_object['tweet'])

        #retrieving sentiments from svm
            sentiment_svm , positive_probability, negative_probability, keywords_svm = self.test_classifier.SVMSingleTweet(tweet)
            svm_classification = [
                {   'Actual-Tweet': tweet,
                    'Predicted-Sentiment': sentiment_svm,
                    'Probability-Positive': positive_probability,
                    'Probability-Negative': negative_probability,
                    'Keywords for Analysis': keywords_svm
                    }
            ]
            x = json.dumps({'SVM Classification': svm_classification})
            json_sentiment_return_svm = json.loads(x)

            sentiment_nvb, keywords_nvb = self.test_classifier.NVBSingleTweet(tweet)
            nvb_classification = [
                { 'Actual-Tweet': tweet,
                  'Predicted-Sentiment': sentiment_nvb,
                  'Keywords for Analysis': keywords_svm
                  }
            ]
            y = json.dumps({'NVB Classification': nvb_classification})
            json_sentiment_return_nvb = json.loads(y)

            credibility_score = self.credibility_checker.core_rating(tweet_object['Author'], tweet_object['tweetId'])

            classification_type_svm = json_sentiment_return_svm.keys()[0]
            sentiment_svm = (json_sentiment_return_svm[classification_type_svm][0]['Predicted-Sentiment']).lower()
            self.es.index(index='sentiment-svm', doc_type='svm-analysis', body={"sentiment": sentiment_svm,
                                                                                "Tweet": tweet_object['tweet'],
                                                                                "Retweet Count": tweet_object['Retweet Count'],
                                                                                "Date": tweet_object['Created Date'],
                                                                                "Author": tweet_object['Author'],
                                                                                "Author Followers Count": tweet_object['Author Follower Count'],
                                                                                "Classification-Type": classification_type_svm,
                                                                                "Credibility-Score": credibility_score})
            print "success"

            classification_type_nvb = json_sentiment_return_nvb.keys()[0]
            sentiment_nvb = (json_sentiment_return_nvb[classification_type_nvb][0]['Predicted-Sentiment']).lower()
            self.es.index(index='sentiment-nvb', doc_type='nvb-analysis', body={"sentiment": sentiment_nvb,
                                                                                "Tweet": tweet_object['tweet'],
                                                                                "Retweet Count": tweet_object['Retweet Count'],
                                                                                "Date": tweet_object['Created Date'],
                                                                                "Author": tweet_object['Author'],
                                                                                "Author Followers Count": tweet_object['Author Follower Count'],
                                                                                "Classification-Type": classification_type_nvb,
                                                                                "Credibility-Score": credibility_score})
            print "success"


x = Analyser()
tweet_collection = x.callFromDatabase()
x.pushToElasticSearch(tweet_collection)