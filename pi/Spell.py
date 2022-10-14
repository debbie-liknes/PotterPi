
class Spell:

    def __init__(self, spellId=-1, spellName="", action=None):
        self.spellName = spellName
        self.action = action
        self.spellId = spellId

    def __lt__(self, other):
        return self.spellId < other.spellId

    def Cast(self):
        print("cast " + self.spellName)
