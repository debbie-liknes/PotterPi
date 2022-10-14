from sklearn import svm
import joblib
from Loader import DataLoader
import cv2
import numpy as np


class Svm:
    def __init__(self):
        self.svm = self.LoadSVMData()
        if self.svm is None:
            self.InitSVM()
        self.Loader = DataLoader
        self.hog = self.InitHOG()

    def InitSVM(self):
        self.svm = svm.SVC(kernel='linear', probability=True)

    def InitHOG(self):
        return cv2.HOGDescriptor((64, 64), (32, 32), (16, 16), (16, 16),
                                 9, 1, -1, 0, 0.2, 0, 64, 1)

    def LoadSVMData(self):
        try:
            return joblib.load('../Data/svm.pkl')
        except:
            return None

    def Train(self, images):
        features = []
        labels = []
        for spellId in images:
            for path in images[spellId]:
                image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                resized = cv2.resize(image, (64, 64), interpolation=cv2.INTER_AREA)

                descriptors = self.hog.compute(resized)
                features.append(descriptors)
                labels.append(int(spellId))

        self.svm.fit(features, labels)
        joblib.dump(self.svm, '../Data/svm.pkl')

    def Predict(self, image):
        resized = cv2.resize(image, (64, 64), interpolation=cv2.INTER_AREA)
        descriptors = self.hog.compute(resized)
        res = self.svm.predict_proba([descriptors])
        probabilities = res[0]
        print(res)
        index = np.argmax(probabilities)
        maxProb = probabilities[index]
        return maxProb, index
