from collections import UserDict
from pickle import load, dump


FILE_NAME = 'notebook.pickle'


class Notebook(UserDict):
    def __init__(self):
        self.data = {}
        self.load_data()

    def load_data(self):
        try:
            with open(FILE_NAME, 'rb') as fh:
                self.data = load(fh)
        except FileNotFoundError:
            pass

    def save_data(self):
        with open(FILE_NAME, 'wb') as fh:
            dump(self.data, fh)
