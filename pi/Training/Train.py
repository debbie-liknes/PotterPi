from Training.SpellLoader import SpellLoader
from Training.skSvm import Svm
import os
import cv2


class Train:
    def __init__(self):
        self.spellLoader = SpellLoader()
        self.spellLoader.Load()
        self.svm = Svm()
        self.svm.LoadSVMData()

    def AddSpell(self, spellName):
        return self.spellLoader.AddSpell(spellName)

    def SaveSpellData(self):
        self.spellLoader.Save()

    def RemoveSpell(self, spell):
        self.spellLoader.RemoveSpell(spell)

    def EditSpellName(self, spell, spellName):
        spell.spellName = spellName
        self.spellLoader.Save()

    def Train(self):
        self.svm.Train(self.spellLoader.paths)

    def AddTrainingImage(self, path, spell):
        image = cv2.imread(path)
        os.remove(path)
        self.spellLoader.AddTrainingImage(image, spell)
        self.spellLoader.Save()
