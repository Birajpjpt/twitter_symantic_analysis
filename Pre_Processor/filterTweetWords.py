import re

class Filter_Tweet_Words:
    def __init__(self):
        self.stopwords = self.stopWordsList()

    def replaceRepetitiveCharacters(self, s):
        pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
        return pattern.sub(r"\1\1", s)

    def stopWordsList(self):
        stopWords = []
        stopWords.append('at_user')
        stopWords.append('url')
        fp = open('../stopwords.txt', 'r')
        line = fp.readline()

        while line:
            word = line.strip()
            stopWords.append(word)
            line = fp.readline()
        #end loop
        fp.close()
        return stopWords

    def getFeatureVector(self, tweet):
        # featureList = []
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
        return featureVector
