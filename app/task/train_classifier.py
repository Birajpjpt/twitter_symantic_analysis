from app.modules.modules import TrainClassifier

if __name__ == "__main__":
    training_model_extractor = TrainClassifier()
    training_model_extractor.NVBclassifier()
    training_model_extractor.SVMClassifier()
