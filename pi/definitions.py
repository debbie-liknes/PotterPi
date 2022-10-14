import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'Data')
IMAGE_DIR = os.path.join(DATA_DIR, 'Images')
SPELL_DATA_FILE = os.path.join(DATA_DIR, "spellsData.yml")
SVM_DATA_FILE = os.path.join(DATA_DIR, "svm.pkl")
