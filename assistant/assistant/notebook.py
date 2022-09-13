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
        if self.tags is not None:
            tag_string = '><'.join(self.tags)
            tag_string = '<' + tag_string + '>'
        result = f'\nNote: {self.__name}\nTag: {tag_string}\n{self.__text_note}'
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

    def edit_text_note(self, new_text: str, add_text=True):
        # new_text = input('Input text:')
        if add_text:
            self.text_note += new_text
        else:
            self.text_note = new_text

    def add_tag(self, value: str):
        if not (value in self.tags):
            self.tags.append(value)

    def del_tag(self, value: str):
        try:
            self.tags.remove(value)
        except ValueError:
            return f"{value} does not exists"

    def change_tag(self, old_value: str, new_value: str):
        if new_value in self.tags:
            return f'Already have a tag <{new_value}>'
        try:
            self.tags.remove(old_value)
            self.tags.append(new_value)
        except ValueError:
            return f"{old_value} does not exists"


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
            raise ValueError(f'Note "{name}" not found')

    def edit_note_text(self, name: str, text_note: str):
        if name in self.data:
            self.data[name].edit_text_note(text_note)
        else:
            raise ValueError(f'Note "{name}" not found')

    def find_note(self, find_text: str):
        find_result = []
        for note in self.data.values():  # type: Note
            # find by name or text
            if find_text in str(note.name) or find_text in str(note.text_note):
                find_result.append(f'"{note.name}"')
        if len(find_result) > 0:
            return f'Notes where "{find_text}" were found: ' + ', '.join(find_result)
        return f'"{find_text}" matches not found'

    def find_note_by_tag(self, find_tag: str):
        find_result = []
        for note in self.data.values():  # type: Note
            # find by name or text
            if find_tag in note.tags:
                find_result.append(f'"{note.name}"')
        if len(find_result) > 0:
            return f'Notes with tag "{find_tag}" were found: ' + ', '.join(find_result)
        return f'Note with tag "{find_tag}" not found'

    def show_note(self):
        for note in self.data.values():
            print(note)

    def show_note_by_tag(self):
        result = {}
        for note in self.data.values():
            for tag in note.tags:
                if not (tag in result):
                    result[tag] = []
                result[tag].append(f'"{note.name}"')
        for key, value in result.items():
            print(f'<{key}>: ' + ', '.join(value))


if __name__ == '__main__':

    print('------ Notebook -------')
    # my_note = Notebook()
    # # my_note.del_note('первый')
    # my_note.add_note('первый', 'первая запись')
    # my_note.add_note('второй', 'вторая запись')
    # # my_note.edit_note_text('первый', 'перезаписаная запись')
    # my_note['первый'].add_tag('temp')
    # my_note['первый'].add_tag('first')
    # my_note['первый'].change_tag('temp', 'second')
    # my_note['второй'].add_tag('second')
    # # my_note.edit_note_text('второй', ' добавленная запись')
    #
    # my_note.save_data()
    #
    # print(my_note.find_note('з'))
    # print(my_note.find_note_by_tag('second'))
    # print('------------')
    # my_note.show_note()
    # my_note.show_note_by_tag()
