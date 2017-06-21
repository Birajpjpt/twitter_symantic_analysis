import nltk
import pickle
from Pre_Processor.feature_extractor import FeatureListExtractor

class TrainClassfier:
    def classifier(self):

        training_set = FeatureListExtractor().trainingSetExtractor('train', '../twitter_training.csv')
        print training_set
        NBClassifier = nltk.NaiveBayesClassifier.train(training_set)
        model = open('../NBclassifier.pickle', 'wb')
        pickle.dump(NBClassifier, model)
        model.close()
        print('Training Complete.......')


