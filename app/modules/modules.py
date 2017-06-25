import re, os, sys
import nltk
import csv
import pickle
import svm
from svmutil import *
from app.location import AbsolutePath


class FilterTweetWords:
    def __init__(self):
        self.stopWordPath = AbsolutePath().stopwords
        self.stopwords = self.stopWordsList()

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

    def replaceRepetitiveCharacters(self, s):
        pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
        return pattern.sub(r"\1\1", s)

    def stopWordsList(self):
        stopWords = []
        stopWords.append('at_user')
        stopWords.append('url')
        fp = open(self.stopWordPath, 'r')
        line = fp.readline()

        while line:
            word = line.strip()
            stopWords.append(word)
            line = fp.readline()
        #end loop
        fp.close()
        return stopWords

    def getFeatureVector(self, tweet):
        featureVector = []
        for w in tweet.split():
            w = self.replaceRepetitiveCharacters(w)
            w = w.strip('\'"?,.')
            val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
            if w in self.stopwords or val is None:
                continue
            else:
                featureVector.append(w.lower())
                # featureList.append(w.lower())
        return list(set(featureVector))


class FeatureListExtractor:
    def __init__(self):
        self.filterTweetWords = FilterTweetWords()
        self.featureList = []
        self.training_file = AbsolutePath().training_file
        self.getFeatureVectorSentiment(self.training_file)

    def extractFeatures(self, tweet):
        tweet_words = set(tweet)
        features = {}
        if not self.featureList:
            self.getFeatureVectorSentiment(self.training_file)
        for word in self.featureList:
            features['contains(%s)' % word] = word in tweet_words
        return features

    def NVBTrainingSetExtractor(self, csvFile):
        stopWords = self.filterTweetWords.stopWordsList()
        tweets = self.getFeatureVectorSentiment(csvFile)
        training_set = nltk.classify.util.apply_features(self.extractFeatures, tweets)
        return training_set

    def getFeatureVectorSentiment(self, csvFile):
        allTweetsSentiments = csv.reader(open(csvFile, 'rb'), delimiter=',')
        stopWords = self.filterTweetWords.stopWordsList()
        tweets = []
        for row in allTweetsSentiments:
            sentiment = row[0]
            tweet = row[1]
            processedTweet = self.filterTweetWords.processTweet(tweet)
            featureVector = self.filterTweetWords.getFeatureVector(processedTweet)
            self.featureList.extend(featureVector)
            tweets.append((featureVector, sentiment));
        self.featureList = list(set(self.featureList))
        return tweets

    def SVMTrainingSetExtractor(self, csvFile):

        tweets = self.getFeatureVectorSentiment(csvFile)
        sortedFeatures = sorted(self.featureList)
        map = {}
        feature_vector = []
        labels = []
        for t in tweets:
            label = 0
            # map = {}
            for w in sortedFeatures:
                map[w] = 0

            tweet_words = t[0]
            sentiment = t[1]

            for word in tweet_words:
                if word in map:
                    map[word] = 1

            values = map.values()
            feature_vector.append(values)
            if(sentiment == 'positive'):
                label = 1
            elif(sentiment == 'negative'):
                label = 0
            labels.append(label)

        return {'feature_vector' : feature_vector, 'labels': labels}


class TrainClassifier:
    def __init__(self):
        self.location = AbsolutePath()
        self.training_file = self.location.training_file
        self.nbClassifier = self.location.nbClassifier
        self.svmClassifier = self.location.svmClassifier
        self.featureListExtractor = FeatureListExtractor()

    def NVBclassifier(self):
        training_set = self.featureListExtractor.NVBTrainingSetExtractor(self.training_file)
        NBClassifier = nltk.NaiveBayesClassifier.train(training_set)
        model = open(self.nbClassifier, 'wb')
        pickle.dump(NBClassifier, model)
        model.close()
        print('NVB Training Complete......')

    def SVMClassifier(self):
        result = self.featureListExtractor.SVMTrainingSetExtractor(self.training_file)
        problem = svm_problem(result['labels'], result['feature_vector'])
        param = svm_parameter('-q -b 1')
        param.kernel_type = LINEAR
        classifier = svm_train(problem, param)
        svm_save_model(self.svmClassifier, classifier)
        print ('SVM Training Complete.....')


