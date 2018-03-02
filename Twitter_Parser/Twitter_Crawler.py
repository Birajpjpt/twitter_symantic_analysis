
import tweepy
from tweepy import OAuthHandler
import json
from pymongo import MongoClient
from datetime import *
from dateutil.relativedelta import relativedelta


class Twitter:
    def __init__(self):
    #loading the keys and secret from json file
        apiKeySet = json.loads(open('./../API_Keys.json').read())

        consumer_key = apiKeySet['consumer_key']
        consumer_secret = apiKeySet['consumer_secret']
        access_token = apiKeySet['access_token']
        access_secret = apiKeySet['access_secret']

        # setting up OAuth and API handler for Tweepy
        self.auth = OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_secret)

        self.api = tweepy.API(self.auth,
                         wait_on_rate_limit=True)
        self.client = MongoClient('localhost', 27017)

    def pushTweetToDb(self):

        db = self.client['wannacry_db_live']
        posts = db.tweets
        count = 0
        for raw_data in tweepy.Cursor(self.api.search, q="wannacry").items():
            data_json = raw_data._json
            if 'retweeted_status' in data_json:
                continue
            else:
                try:
                    screenName = data_json['user']['screen_name']
                    tweetId = data_json['id']
                    tweet = str(data_json['text'])
                    post_data = {
                        'tweet': tweet,
                        'Author': screenName,
                        'Author Follower Count': data_json['user']['followers_count'],
                        'Retweet Count': data_json['retweet_count'],
                        'Language': data_json['lang'],
                        'Created Date': data_json['created_at'],
                        'tweetId': tweetId
                    }
                    result = posts.insert_one(post_data)
                    count = count + 1
                    print count

                except:
                    continue

    def query_db(self):
        db = self.client['test']
        posts = db.tweets
        x =posts.find_one({"tweetId": str(889935155896471553)})
        # x =posts.find()
        print x
        # for y in x:
        #     print y


    def sourceCredibility(self, screenName):
        user = self.api.get_user(screenName)
        user_data = user._json
        follower_count = user_data['followers_count']
        if user_data['friends_count'] == 0:
            follower_followee_ratio = 0
        else:
            follower_followee_ratio = user_data['followers_count']/user_data['friends_count']
        account_created_date = (datetime.strptime(user_data['created_at'], '%a %b %d %H:%M:%S +0000 %Y')).strftime('%Y-%m-%d')
        account_created_date = datetime.strptime(account_created_date, '%Y-%m-%d')
        created_days = (datetime.today() -account_created_date).days
        rating = 0
        if user_data['verified']:
            rating = rating + 2

        if follower_count > 2500:
            rating = rating + 2

        if follower_count > 500 and follower_count <= 2500:
            rating = rating + 1

        if follower_followee_ratio > 1 and follower_followee_ratio  < 50 :
            rating = rating + 1

        if follower_followee_ratio  >= 50:
            rating = rating + 2

        if created_days > 180 and created_days < 730:
            rating = rating + 1

        if created_days >= 730:
            rating = rating + 2

        if not user_data['default_profile']:
            rating = rating + 1

        if user_data['description'] is not None:
            rating = rating + 1

        # print rating

        return rating, screenName

    def tweetCredibility(self, tweetId):
        tweet = self.api.get_status(tweetId)
        tweet_data = tweet._json
        rating = 0

        if tweet_data['retweet_count'] > 50:
            rating = rating + 1

        if tweet_data['favorite_count'] > 10:
            rating = rating + 1

        if len(tweet_data['entities']['urls']) >= 1:
            rating = rating + 1

        if len(tweet_data['entities']['hashtags']) >= 1:
            rating = rating + 1

        if len(tweet_data['text']) >= 75:
            rating = rating + 1

        return rating, tweet_data['text']

    def core_rating(self, screen_name, tweet_id):
        tweet_rating, tweet = self.tweetCredibility(tweet_id)
        user_rating, username = self.sourceCredibility(screen_name)
        rating = tweet_rating + user_rating
        return rating
        # print "Tweet : \n\n\t\t\t" + str(tweet) + " \n\nTweeted By: \n\n\t\t\t" + str(username) + "\n\nRating : \n\n\t\t" + str(rating)

# x = Twitter()
# # x.pushLiveTweetsToDb()
# x.core_rating('troyhunt', 891595277966098433)
# # x.tweetCredibility('889195992737869824')
# # x.pushTweetToDb()
# x.pushTweetToDb()
# x.sourceCredibility('ComputingNapier')

# x.sourceCredibility(data)
# rate_limit_status = api.rate_limit_status()
# remaining_api_count = rate_limit_status['resources']['search']['/search/tweets']['remaining']
# self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
# self.test_classifier = test_classifier()

# self.tweetCredibility(tweetId)
# self.sourceCredibility(screenName)


# from elasticsearch import Elasticsearch
# import requests
# import sys
# # from app.task.test_classifier import test_classifier
# import time
# import pandas
# import os
# # import datetime