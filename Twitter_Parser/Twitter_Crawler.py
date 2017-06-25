import pandas
import os
import tweepy
from tweepy import OAuthHandler
import time
import json
from elasticsearch import Elasticsearch
import requests


from pprint import pprint

es = Elasticsearch([{'host': 'ec2-54-157-23-248.compute-1.amazonaws.com', 'port': 9200}])

class Twitter:

#loading the keys and secret from json file
    apiKeySet = json.loads(open('./../API_Keys.json').read())

    consumer_key = apiKeySet['consumer_key']
    consumer_secret = apiKeySet['consumer_secret']
    access_token = apiKeySet['access_token']
    access_secret = apiKeySet['access_secret']


    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)


    api = tweepy.API(auth,
                     wait_on_rate_limit=True)

    rate_limit_status = api.rate_limit_status()
    remaining_api_count = rate_limit_status['resources']['search']['/search/tweets']['remaining']
    count = 0
    x = tweepy.Cursor(api.search,
                      q='wannacrypt',
                      include_entities=True).items()

    # while True:
    #     try:
    #         tweet = x.next()
    #         print tweet
    #     except tweepy.TweepError:
    #         print remaining_api_count
    #         time.sleep(60*15)
    #         continue
    #     except StopIteration:
    #         break
    for raw_data in tweepy.Cursor(api.search, q="wannacrypt").items(1):
        data = json.dumps(raw_data._json)
        # print tweet.Status
        count = count + 1
        print count

    print remaining_api_count

    #  print json.dumps(rate_limit_status, indent=4, sort_keys=True)
