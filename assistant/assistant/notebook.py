from collections import UserDict
from pickle import load, dump
from pathlib import Path


FILE_NAME = 'notebook.pickle'


class Note:
    def __init__(self, name: str, text_note: str = None):
        self.__name = None
        self.__text_note = None
        self.tags: list = []

        self.__name = name
        self.__text_note = text_note

    def __str__(self):
        result = f'\nNote: {self.__name}\n{self.__text_note}'
        return result

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name

    @property
    def text_note(self):
        return self.__text_note

    @text_note.setter
    def text_note(self, text_note: str):
        self.__text_note = text_note


class Notebook(UserDict):
    def __init__(self):
        self.data = {}
        self.load_data()

    def load_data(self):
        path = Path('~').expanduser()
        try:
            with open(path / FILE_NAME, 'rb') as fh:
                self.data = load(fh)
        except FileNotFoundError:
            pass

    def save_data(self):
        path = Path('~').expanduser()
        try:
            with open(path / FILE_NAME, 'wb') as fh:
                dump(self.data, fh)
        except Exception:
            print("Some problems!")

    def add_note(self, name: str, text_note: str = None):
        if not (name in self.data):
            self.data[name] = Note(name=name, text_note=text_note)

    def del_note(self, name: str):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f'Note "{name}" not found')

    def edit_note_text(self, name: str, text_note: str):
        if name in self.data:
            self.data[name].text_note = text_note
        else:
            raise KeyError(f'Note "{name}" not found')

    # def find_note(self, find_text: str):
    #     find_result = []
    #     for note in self.data.name():  # type: Note
    #         # find by name or text
    #         if find_text in str(note.name) or bool(
    #                 list(filter(lambda x: find_text in x.value, note.phone_list))):
    #             find_result.append(note.name)
    #     if len(find_result) > 0:
    #         return f'Records where "{find_text}" were found: ' + ', '.join(self.find_result)
    #     return f'"{find_text}" matches not found'

    def show_note(self):
        for note in self.data.values():
            print(note)


if __name__ == '__main__':

    my_note = Notebook()
    my_note.add_note('второй', 'вторая запись')
    my_note.edit_note_text('первый', 'перезаписаная запись')
    my_note.save_data()
    my_note.show_note()
