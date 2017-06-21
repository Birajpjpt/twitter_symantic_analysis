import re

class Preprocessor:

    #start process_tweet
    def processTweet(self, tweet):

        tweet = str(tweet)
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)
        tweet = re.sub('@[^\s]+','AT_USER',tweet)
        tweet = re.sub('[\s]+', ' ', tweet)
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
        tweet = tweet.strip('\'"')
        tweet = [e.lower() for e in tweet.split() if len(e)>=3]
        tweet = ' '.join(tweet)
        return tweet