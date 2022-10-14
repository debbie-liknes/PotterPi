from Training.SpellLoader import SpellLoader
from Training.skSvm import Svm


class SpellMatch:
    def __init__(self):
        self.spellLoader = SpellLoader()
        self.spellLoader.Load()
        self.svm = Svm()
        self.svm.LoadSVMData()

    def RecognizeSpell(self, image):
        prob, index = self.svm.Predict(image)
        if prob > 0.6:
            return self.spellLoader.spells[index]
        return None
