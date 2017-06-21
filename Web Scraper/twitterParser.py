import tweepy
from tweepy import OAuthHandler
import json

consumer_key = 'UtFuZYdL9nqS5qZvGFs7d5stH'
consumer_secret = 'I9tja5pxBaFYvE4enbo84wNeDIMtirWJeQeAplciQuVskr3uSZ'
access_token = '121073371-cKt1U5Tson0Zb0esWFGYjngs4kaqgNZ859pj1bcs'
access_secret = 'Fei5jkxPsr5czRBArp4Nz3l54ftIudkoVvHhNb0qxmG3s'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

# for friend in tweepy.Cursor(api.friends).items(1):
#    print friend._json['screen_name']

print api.search

for search in tweepy.Cursor(api.search).items(1):
    print search