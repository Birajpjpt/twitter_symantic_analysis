import json
import tweepy
from tweepy import OAuthHandler

class set_twitter_config:

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

class streamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        if status_code == 420:
            return False

twitter_config = set_twitter_config()
stream_listener = streamListener()
stream = tweepy.Stream(auth=twitter_config.api.auth, listener=streamListener)
stream.filter(track=['wannacrypt'])