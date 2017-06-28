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


from pprint import pprint

# es = Elasticsearch([{'host': 'ec2-54-157-23-248.compute-1.amazonaws.com', 'port': 9200}])

class Twitter:

    def __init__(self):


    #loading the keys and secret from json file
        apiKeySet = json.loads(open('./../API_Keys.json').read())

        consumer_key = apiKeySet['consumer_key']
        consumer_secret = apiKeySet['consumer_secret']
        access_token = apiKeySet['access_token']
        access_secret = apiKeySet['access_secret']


        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)


        self.api = tweepy.API(auth,
                         wait_on_rate_limit=True)

        # rate_limit_status = api.rate_limit_status()
        # remaining_api_count = rate_limit_status['resources']['search']['/search/tweets']['remaining']


        count = 0
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        self.test_classifier = test_classifier()

    def pushTweetToDb(self):

        for raw_data in tweepy.Cursor(self.api.search, q="wannacrypt").items():
            data_json = raw_data._json
            count = count + 1
            if 'retweeted_status' in data_json:
                continue
            else:
                try:
                    tweet = str(data_json['text'])

                    #retrieving sentiments from svm
                    sentiment_svm , positive_probability, negative_probability,  keywords_svm = test_classifier.SVMSingleTweet(tweet)
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

                    sentiment_nvb, keywords_nvb = test_classifier.NVBSingleTweet(tweet)
                    nvb_classification = [
                        { 'Actual-Tweet': tweet,
                          'Predicted-Sentiment': sentiment_nvb,
                          'Keywords for Analysis': keywords_svm
                          }
                    ]
                    y = json.dumps({'NVB Classification': nvb_classification })
                    json_sentiment_return_nvb = json.loads(y)

                    classification_type_svm = json_sentiment_return_svm.keys()[0]
                    sentiment_svm = (json_sentiment_return_svm[classification_type_svm][0]['Predicted-Sentiment']).lower()
                    es.index(index='sentiment-svm', doc_type='svm-analysis', body={"sentiment": sentiment_svm,
                                                                                   "Tweet": data_json['text'],
                                                                                   "Author": data_json['user']['screen_name'],
                                                                                   "Date": data_json['created_at'],
                                                                                   "Classification-Type": classification_type_svm})

                    classification_type_nvb = json_sentiment_return_nvb.keys()[0]
                    sentiment_nvb = (json_sentiment_return_nvb[classification_type_nvb][0]['Predicted-Sentiment']).lower()
                    es.index(index='sentiment-nvb', doc_type='nvb-analysis', body={"sentiment": sentiment_nvb,
                                                                               "Tweet": data_json['text'],
                                                                               "Author": data_json['user']['screen_name'],
                                                                               "Date": data_json['created_at'],
                                                                               "Classification-Type": classification_type_nvb})

                    print tweet
                except:
                    continue

    print count
    print "Success"

