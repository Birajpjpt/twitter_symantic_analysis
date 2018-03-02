import tweepy
from tweepy import OAuthHandler
import json
from pymongo import MongoClient
from tweepy import Stream


class StreamListener(tweepy.StreamListener):

    def __init__(self):
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


    def on_status(self, status):
        db = self.client['tweet_listener_test']
        posts = db.tweets
        count = 0
        if hasattr(status, "retweeted_status"):
            return
        else:
            try:
                screenName = status.user.screen_name
                tweetId = status.id
                tweet = str(status.text)
                post_data = {
                    'tweet': tweet,
                    'Author': screenName,
                    'Author Follower Count': status.user.followers_count,
                    'Retweet Count': status.retweet_count,
                    'Language': status.lang,
                    'Created Date': status.created_at,
                    'tweetId': tweetId
                }
                result = posts.insert_one(post_data)
                print "Tweet pushed to Db Test: " + str(tweetId)
                count = count + 1
                if count == 20:
                    print '\n\n\n\n\n\n\n'
            except:
                return

    def on_error(self, status_code):
        if status_code == 420:
            return False

    def liveTweetListener(self):
        stream_listener = StreamListener()
        stream = Stream(auth=self.auth, listener=stream_listener)
        stream.filter(track=['wannacry'])

    def query_db(self):
        db = self.client['tweet_listener_test']
        posts = db.tweets
        x =posts.find_one({"tweetId": 889946961276809217})
        # x =posts.find()
        print x
        # for y in x:
        #     print y





x = StreamListener()
x.query_db()