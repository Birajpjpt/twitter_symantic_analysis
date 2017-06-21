import tweepy
from tweepy import OAuthHandler

class Authenticator(object):
    def __init__(self):
        self.consumer_key = 'UtFuZYdL9nqS5qZvGFs7d5stH'
        self.consumer_secret = 'I9tja5pxBaFYvE4enbo84wNeDIMtirWJeQeAplciQuVskr3uSZ'
        self.access_token = '121073371-cKt1U5Tson0Zb0esWFGYjngs4kaqgNZ859pj1bcs'
        self.access_secret = 'Fei5jkxPsr5czRBArp4Nz3l54ftIudkoVvHhNb0qxmG3s'
        self.auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_secret)

    def api(self):
        self.api = tweepy.API(self.auth)