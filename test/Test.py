import unittest
from app.modules.modules import *
import os.path
from app.task.test_classifier import *

class TestFilterTweets(unittest.TestCase):

    testTweet = '@skynews I know that wannacrypt is the worse ransomware. #wannacrypt https://youtube.com/wannacrypt'
    filterTweet = FilterTweetWords()

    def test_filterTweetWordsGetsStopWordsFileLocation(self):
        self.assertEqual(self.filterTweet.stopWordPath, '/Users/prajapatib/Dissertation/twitter_symantic_analysis/app/data_files/stopwords.txt')

    def test_filterTweetWordsInitiatesAllStopWords(self):
        self.assertIsNot(len(self.filterTweet.stopwords), 0)
        self.assertIn('has', self.filterTweet.stopwords)

    def test_processTweetReturnsString(self):
        filtered_tweet = self.filterTweet.processTweet(self.testTweet)
        self.assertIsInstance(filtered_tweet, basestring)

    def test_processTweetReducesNoise(self):
        filtered_tweet = self.filterTweet.processTweet(self.testTweet)
        self.assertNotIn('is', filtered_tweet)
        self.assertNotIn('https://youtube.com/wannacrypt', filtered_tweet)
        self.assertNotIn('#wannacrypt', filtered_tweet)
        self.assertNotIn('@skynews', filtered_tweet)
        self.assertIn('url', filtered_tweet)
        self.assertIn('at_user', filtered_tweet)

    def test_RepetitiveCharactersReplaced(self):
        test_word = 'hurrrrray!!!'
        self.assertEqual(self.filterTweet.replaceRepetitiveCharacters(test_word), 'hurray!!')

    def test_getFeatureVectorReturnsList(self):
        self.assertIsInstance(self.filterTweet.getFeatureVector(self.filterTweet.processTweet(self.testTweet)), list)

    def test_getFeatureVectorReturnsFilteredWords(self):
        processedTweet = self.filterTweet.processTweet(self.testTweet)
        self.assertNotIn('at_user', self.filterTweet.getFeatureVector(processedTweet))
        self.assertIn('wannacrypt', self.filterTweet.getFeatureVector(processedTweet))

class TestFeatureListExtractor(unittest.TestCase):
    testTweet = '@skynews I know that wannacrypt is the worse ransomware. #wannacrypt https://youtube.com/wannacrypt'
    filterTweet = FilterTweetWords()
    tweet_features = filterTweet.getFeatureVector(filterTweet.processTweet(testTweet))
    featureListExtractor = FeatureListExtractor()
    trainingFile = featureListExtractor.training_file

    def test_featureListExtractorGetsTrainingFileLocation(self):
        self.assertEqual(self.featureListExtractor.training_file, '/Users/prajapatib/Dissertation/twitter_symantic_analysis/app/data_files/twitter_training.csv')

    def test_featureListExtractorPopulatesFeatureList(self):
        self.assertIsNot(len(self.featureListExtractor.featureList), 0)

    def test_extractFeaturesReturnsDict(self):
        self.assertIsInstance(self.featureListExtractor.extractFeatures(self.tweet_features), dict)

    def test_extractFeaturesReturnsFeatures(self):
        self.assertIn('contains(worse)', self.featureListExtractor.extractFeatures(self.tweet_features))
        self.assert_(self.featureListExtractor.extractFeatures(self.tweet_features)['contains(worse)'])

    def test_getFeatureVectorSentimentReturnsList(self):
        self.assertIsInstance(self.featureListExtractor.getFeatureVectorSentiment(self.trainingFile), list)

    def test_getFeatureVectorSentimentReturnsKeywordsAndSentiment(self):
        self.assertEqual(len(self.featureListExtractor.getFeatureVectorSentiment(self.trainingFile)[0]), 2)

    def test_NVBExtractorReturnsNltkLazyMap(self):
        self.assertIsInstance(self.featureListExtractor.NVBTrainingSetExtractor(self.trainingFile), nltk.collections.LazyMap)

    def test_NVBExtractorReturnsNonEmptyTrainingSet(self):
        self.assertNotEqual(len(self.featureListExtractor.NVBTrainingSetExtractor(self.trainingFile)), 0)
        self.assertNotEqual(len(self.featureListExtractor.NVBTrainingSetExtractor(self.trainingFile)[0]), 0)

    def test_SVMExtractorReturnsDict(self):
        self.assertIsInstance(self.featureListExtractor.SVMTrainingSetExtractor(self.trainingFile), dict)

    def test_SVMExtractorReturnsNonEmptyTrainingSet(self):
        self.assertNotEqual(len(self.featureListExtractor.SVMTrainingSetExtractor(self.trainingFile)), 0)
        self.assertNotEqual(len(self.featureListExtractor.SVMTrainingSetExtractor(self.trainingFile)['feature_vector']), 0)
        self.assertNotEqual(len(self.featureListExtractor.SVMTrainingSetExtractor(self.trainingFile)['labels']), 0)

class TestTrainClassifier(unittest.TestCase):
    trainClassifier = TrainClassifier()
    trainingFile = trainClassifier.training_file

    def test_featureListExtractorGetsTrainingFileLocation(self):
        self.assertEqual(self.trainClassifier.training_file, '/Users/prajapatib/Dissertation/twitter_symantic_analysis/app/data_files/twitter_training.csv')

    def test_NVBClassifierOutputsModel(self):
        self.trainClassifier.NVBclassifier()
        self.assert_(os.path.exists(self.trainClassifier.nbClassifier))

    def test_SVMClassifierOutputsModel(self):
        self.trainClassifier.SVMClassifier()
        self.assert_(os.path.exists(self.trainClassifier.svmClassifier))

class TestLocation(unittest.TestCase):
    location = AbsolutePath()

    def test_AbsolutePathInitiatesAllPaths(self):
        self.assertEqual(self.location.training_file, '/Users/prajapatib/Dissertation/twitter_symantic_analysis/app/data_files/twitter_training.csv' )
        self.assertEqual(self.location.testing_file, '/Users/prajapatib/Dissertation/twitter_symantic_analysis/app/data_files/testing_file.csv' )
        self.assertEqual(self.location.stopwords, '/Users/prajapatib/Dissertation/twitter_symantic_analysis/app/data_files/stopwords.txt' )
        self.assertEqual(self.location.svmClassifier, '/Users/prajapatib/Dissertation/twitter_symantic_analysis/app/classifier/SVMClassifier' )
        self.assertEqual(self.location.nbClassifier, '/Users/prajapatib/Dissertation/twitter_symantic_analysis/app/classifier/NBclassifier.pickle' )

class TestClassifiers(unittest.TestCase):
    testClassifier = test_classifier()
    testTweet = '@skynews I know that wannacrypt is the worse ransomware. #wannacrypt https://youtube.com/wannacrypt'

    def test_nvbSingleTweetReturnsStringAndList(self):
        nvbSentiment, nvbKeywords = self.testClassifier.NVBSingleTweet(self.testTweet)
        self.assertIsInstance(nvbSentiment, basestring)
        self.assertIsInstance(nvbKeywords, list)

    def test_nvbSingleTweetReturnsSentiment(self):
        nvbSentiment, nvbKeywords = self.testClassifier.NVBSingleTweet(self.testTweet)
        self.assert_(nvbSentiment == 'positive' or nvbSentiment == 'negative')

    def test_svmSingleTweetReturnsStringFloatsList(self):
        svmSentiment, positiveProbs, negativeProbs, keywords = self.testClassifier.SVMSingleTweet(self.testTweet)
        self.assertIsInstance(svmSentiment, basestring)
        self.assertIsInstance(positiveProbs and negativeProbs, basestring)
        self.assertIsInstance(keywords, list)

    def test_svmSingleTweetReturnsSentiment(self):
        svmSentiment, positiveProbs, negativeProbs, keywords = self.testClassifier.SVMSingleTweet(self.testTweet)
        self.assert_(svmSentiment == 'positive' or svmSentiment == 'Negative')

if __name__ == '__main__':
    unittest.main()
