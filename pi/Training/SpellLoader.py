import yaml
from Loader import DataLoader
from Spell import Spell
import cv2
import os
import definitions


class SpellLoader:
    def __init__(self):
        self.spells = []
        self.paths = {}
        self.nextId = 0
        self.Loader = DataLoader

    def Load(self):
        with open(definitions.SPELL_DATA_FILE, "r") as stream:
            try:
                doc = yaml.load(stream, self.Loader)
                if doc is not None:
                    spells = doc.get("spells")
                    paths = doc.get("paths")
                    self.nextId = doc.get("nextId")

                    if spells is not None:
                        for spell in spells:
                            self.spells.append(spell)
                        self.spells.sort()
                    if paths is not None:
                        for spellId in paths:
                            self.paths[spellId] = paths[spellId]
            except yaml.YAMLError as exc:
                print(exc)

    def AddSpell(self, spellName):
        for s in self.spells:
            if spellName == s.spellName:
                return False
        self.spells.append(Spell(spellName=spellName, spellId=self.nextId))
        self.nextId += 1
        return True

    def RemoveSpell(self, spell):
        self.spells.remove(spell)
        for path in self.paths[spell.spellId]:
            os.remove(path)
        self.paths.pop(spell.spellId)

    def GenerateTrainingFileName(self, spellId):
        retVal = 0
        ids = self.paths.get(spellId)
        if ids is not None:
            retVal = len(ids)
        return str(spellId) + "_" + str(retVal) + ".jpg"

    def AddTrainingImage(self, image, spell):
        newFile = self.GenerateTrainingFileName(spell.spellId)
        path = definitions.IMAGE_DIR + "\\" + newFile
        cv2.imwrite(path, image)
        if self.paths.get(spell.spellId) is not None:
            self.paths[spell.spellId].append(path)
        else:
            self.paths[spell.spellId] = [path]

    def Save(self):
        spellDict = {"spells": self.spells, "paths": self.paths, "nextId": self.nextId}
        with open(definitions.SPELL_DATA_FILE, 'w') as outfile:
            yaml.dump(spellDict, outfile, default_flow_style=False)
