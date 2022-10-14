import cv2
from Training.Train import Train


class TrainCLI:
    def __init__(self):
        self.trainer = Train()

    def run(self):
        while True:
            print()
            print("Select option with number keys")
            print("\t1. View/Train Spells")
            print("\t2. Add spell")
            print("\t3. Run Training")
            print("\t4. Test Prediction")
            print("\tAny other key to exit")

            val = input()

            if val == '1':
                self.ShowSpells()
            elif val == '2':
                self.AddSpell()
            elif val == '3':
                self.trainer.Train()
            elif val == '4':
                path = input("Path to image: ")
                image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                val, spellIndex = self.trainer.svm.Predict(image)
                print("Spell is index " + str(spellIndex))
                print(str(val * 100) + "% confident ")

            else:
                break

    def AddSpell(self):
        name = input("Spell Name: ")
        if self.trainer.AddSpell(name):
            self.trainer.SaveSpellData()
        else:
            print("Spell already exists")

    def ShowSpells(self):
        print()
        print("Select spell to edit or add image, enter to go back")
        spells = self.trainer.spellLoader.spells
        for spell in spells:
            print(str(spell.spellId) + "." + spell.spellName)
        val = input()
        try:
            choice = int(val)
            for spell in spells:
                if spell.spellId == choice:
                    self.ModifySpell(spells[choice])
                    return
        except:
            return

    def ModifySpell(self, spell):
        print()
        print("Edit or Train spell - " + spell.spellName)
        print("1.Edit Name")
        print("2.Add training image")
        print("3.Delete Spell")
        val = input()
        try:
            choice = int(val)

            if choice == 1:
                name = input("New Spell Name: ")
                self.trainer.EditSpellName(spell, name)
            if choice == 2:
                path = input("Path to image: ")
                self.trainer.AddTrainingImage(path, spell)
            if choice == 3:
                self.trainer.RemoveSpell(spell)
                self.trainer.SaveSpellData()
        except:
            return


cli = TrainCLI()
cli.run()
