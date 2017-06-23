import os

class AbsolutePath:
    def __init__(self):
        self.training_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data_files/twitter_training.csv')
        self.testing_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data_files/testing_file.csv')
        self.stopwords = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data_files/stopwords.txt')
        self.nbClassifier = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'classifier/NBclassifier.pickle')
        self.svmClassifier = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'classifier/SVMClassifier')
