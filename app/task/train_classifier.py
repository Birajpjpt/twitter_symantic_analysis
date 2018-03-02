from app.modules.modules import TrainClassifier
import time

if __name__ == "__main__":
    training_model_extractor = TrainClassifier()
    t0 = time.time()
    training_model_extractor.NVBclassifier()
    t1 = time.time()
    print "Training Time for NVB: \t" + str(t1-t0) + " Seconds \n\n\n"
    t2 = time.time()
    training_model_extractor.SVMClassifier()
    t3 = time.time()
    print "Training Time for SVM: \t" + str(t3-t2) + " Seconds"
