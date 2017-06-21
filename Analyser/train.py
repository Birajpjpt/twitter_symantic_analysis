from Algorithm.NB_classifier import TrainClassfier
from Algorithm.SVM_Classifier import SVM_Classifier

if __name__ == "__main__":
    NBclassifier = TrainClassfier()
    NBclassifier.classifier()

    SVMClassifier = SVM_Classifier()
    SVMClassifier.trainClassifier()
