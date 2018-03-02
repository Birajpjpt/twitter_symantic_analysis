from got.manager.TweetCriteria import *
from got.manager.TweetManager import *


class Scraper:

    def __init__(self):
        self.scraper = TweetCriteria()
        self.twitter_query_manager = TweetManager()

    def getTweets(self):
        criteria = self.scraper.setQuerySearch('wannacry')\
                                .setSince("2017-05-12")\
                                .setUntil("2017-05-13")\
                                .setMaxTweets(1000)
        tweet = self.twitter_query_manager.getTweets(criteria)

        for t in tweet:
            print t

x = Scraper()
x.getTweets()