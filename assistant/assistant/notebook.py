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
        tag_string = ''
        if len(self.tags) > 0:
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


class Notebook(UserDict):
    def __init__(self):
        super().__init__()
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
        if name == '':
            raise ValueError('Name cannot be empty')
        if not (name in self.data.keys()):
            self.data[name] = Note(name=name, text_note=text_note)
            input_text = input('Input text note:')
            self.data[name].text_note = input_text
        else:
            raise ValueError('This name already exists')

    def del_note(self, name: str):
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError(f'Note "{name}" not found')

    def edit_note_tag(self, name: str):
        if name in self.data.keys():
            print(self.data[name])
            flag = input('input add or delete tag (a/d)')
            if flag == 'a':
                tag = input('input new tag: ')
                self.data[name].add_tag(tag)
            else:
                tag = input('input remove tag: ')
                self.data[name].del_tag(tag)
        else:
            raise ValueError(f'Note "{name}" not found')

    def edit_note_text(self, name: str):
        if name in self.data.keys():
            print(self.data[name])
            text_note = input('>')
            flag = input('input add or overwrite text (a/o)')
            self.data[name].edit_text_note(text_note, add_text=False) if flag == 'o' \
                else self.data[name].edit_text_note(text_note)
        else:
            raise ValueError(f'Note "{name}" not found')

    def find_note(self, find_text: str):
        find_result = []
        for note in self.data.values():  # type: Note
            # find by name or text
            if find_text.lower() in str(note.name).lower() or find_text.lower() in str(note.text_note).lower():
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
            if find_tag == '' and len(note.tags) == 0:
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
            if len(note.tags) == 0:
                if not ('' in result.keys()):
                    result[''] = []
                result[''].append(f'"{note.name}"')
            for tag in note.tags:
                if not (tag in result.keys()):
                    result[tag] = []
                result[tag].append(f'"{note.name}"')
        for key, value in result.items():
            print(f'<{key}>: ' + ', '.join(value))


this_notebook = Notebook()

