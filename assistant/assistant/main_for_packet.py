from typing import Dict, Callable
from collections import UserDict
from datetime import datetime, timedelta
from pickle import load, dump
from pathlib import Path


FILE_NAME = 'notebook.pickle'
FILE_NAME_2 = 'contacts_book.pickle'


class Field:
    def __init__(self, value: str):
        self.__value = None

        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Birthday(Field):
    def __init__(self, value: datetime):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        if len(value) == 0:
            raise ValueError('Name length must be greater than 0')
        if '.' in value:
            Field.value.fset(self, datetime.strptime(value, '%d.%m.%Y'))
        elif '/' in value:
            Field.value.fset(self, datetime.strptime(value, '%d/%m/%Y'))
        else:
            raise ValueError('Date must be in the format "dd/mm/yyyy" or "dd.mm.yyyy"')


class Name(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        if len(value) > 0:
            Field.value.fset(self, value)
        else:
            raise ValueError('Name length must be greater than 0')


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        if len(value) == 0:
            raise ValueError('Phone length must be greater than 0')
        if len(value) == 9 and str(value).isdigit():
            value = '+380' + str(value)
            Field.value.fset(self, value)
        elif len(value[1::]) == 12 and str(value[1::]).isdigit() and value[0] == '+':
            Field.value.fset(self, value)
        else:
            raise ValueError('Phone must be in the format "+############" or "#########"')


class Address(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        if len(value) > 0:
            Field.value.fset(self, value)
        else:
            raise ValueError('Address length must be greater than 0')


class Email(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        user_name, email_box = value.split('@')
        if '@' not in value:
            raise ValueError('Email must contain the @ symbol')
        if len(user_name) <=1:
            raise ValueError('Length name in name@... must be more 1 symbol')
        Field.value.fset(self, value)


class Record:

    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None, address: Address = None, email: Email = None):
        self.name: Name = name
        self.phone_list: list[Phone] = [phone] if phone is not None else []
        self.birthday: Birthday = birthday
        self.address: Address = address
        self.email: Email = email

    def __str__(self):
        result = f"{self.name.value}:"
        if len(self.phone_list) > 0:
            result += f" {', '.join(phone.value for phone in self.phone_list)};"
        if self.email is not None:
            result += f" e-mail: {self.email.value};"
        if self.address is not None:
            result += f" address: {self.address.value};"
        if self.birthday is not None:
            result += f" birthday: {self.birthday.value.strftime('%d.%m.%Y')};"
        result += '\n'
        return result

    def add_phone(self, phone: Phone):
        self.phone_list.append(phone)
        return 'Phone added'

    def change_phone(self, phone: Phone, index: int = 0):
        try:
            self.phone_list[index] = phone
            return 'Number changed successfully'
        except KeyError:
            return f'In field {index} there is no phone number to change'

    def delete_phone(self, phone: Phone):
        try:
            self.phone_list.remove(Phone)
            return 'Number deleted successfully'
        except KeyError:
            return f'In field {self.name.value} there is no phone number to delete'

    def change_phone(self, old_phone: Phone, new_phone: Phone):
        try:
            self.phone_list.remove(old_phone)
            self.phone_list.append(new_phone)
            return 'Number changed successfully'
        except KeyError:
            return f'In field {self.name.value} there is no phone number to delete'

    def show_phone(self):
        return ' '.join([phone.value for phone in self.phone_list])

    def set_address(self, address: Address):
        self.address = address

    def set_email(self, email: Email):
        self.email = email

    def set_birthday(self, birthday: Birthday):
        self.birthday = birthday

    def days_to_birthday(self) -> int:
        if self.birthday is None:
            return None
        birthday = self.birthday.value
        try:
            birthday_this_year = birthday.replace(year=datetime.now().year)
            if birthday_this_year.date() < datetime.now().date():
                birthday_this_year = birthday_this_year.replace(year=datetime.now().year + 1)
            # processing on February 29 by increasing the date of the birthday by 1
        except ValueError:
            birthday += timedelta(days=1)
            birthday_this_year = birthday.replace(year=datetime.now().year)
            if birthday_this_year.date() < datetime.now().date():
                birthday_this_year = birthday_this_year.replace(year=datetime.now().year + 1)
        delta = birthday_this_year.date() - datetime.now().date()
        return delta.days


class AddressBook(UserDict):
    def __init__(self, max_line: int = 3):
        self.data = {}
        self.find_result = []
        self.max_line = max_line
        self.current_value = 0
        self.load_book()

    def iterator(self, max_line: int = 5):
        result = ''
        count = 0
        total_count = 0
        for record in self.data.values():  # type: Record
            count += 1
            total_count += 1
            result = result + str(record)
            if count >= max_line or total_count >= len(self.data):
                yield result
                result = ''
                count = 0

    def add_record(self, name: Name, phone: Phone = None):
        if not (name.value in self.data.keys()):
            self.data[name.value] = Record(name=name, phone=phone)

    def del_record(self, name: Name):
        try:
            del self.data[name.value]
        except KeyError:
            raise ValueError('No record with that name')

    def edit_record(self, name: Name):
        if not (name.value in self.data.keys()):
            raise ValueError('No record with that name')

        command = input('Input field edit (phone/address/email/birthday): ')
        if command == 'phone':
            command_phone = 'input (add/del/change):'
            phone = input('Input phone:')
            if command_phone == 'add':
                self.data[name.value].add_phone(Phone(phone))
            elif command_phone == 'del':
                self.data[name.value].delete_phone(Phone(phone))
            elif command_phone == 'change':
                new_phone = input('Input new phone: ')
                self.data[name.value].change_phone(Phone(phone), Phone(new_phone))
        elif command == 'email':
            email = input('Input e-mail: ')
            self.data[name.value].set_email(Email(email))
        elif command == 'address':
            address = input('Input address: ')
            self.data[name.value].set_address(Address(address))
        elif command == 'birthday':
            birthday = input('Input birthday: ')
            self.data[name.value].set_birthday(Birthday(birthday))

    def find_record(self, find_text: str):
        self.find_result = []
        for record in self.data.values():  # type: Record
            # find by name or phones
            if find_text in str(record.name.value) or bool(list(filter(lambda x: find_text in x.value, record.phone_list))):
                self.find_result.append(record.name.value)
        if len(self.find_result) > 0:
            return f'Records where "{find_text}" were found: ' + ', '.join(self.find_result)
        return f'"{find_text}" matches not found'

    def show_record_with_birthday(self, day: int = 0):
        find_result = []
        for record in self.data.values():
            if int(record.days_to_birthday()) == int(day):
                find_result.append(record.name.value)
        if len(find_result) > 0:
            return f'Birthday records in {day} days: ' + ', '.join(find_result)
        return f'no records with birthdays after {day} days'

    def load_book(self):
        path = Path('~').expanduser()
        try:
            with open(path / FILE_NAME_2, 'rb') as fh:
                self.data = load(fh)
        except FileNotFoundError:
            pass

    def save_book(self):
        path = Path('~').expanduser()
        try:
            with open(path / FILE_NAME_2, 'wb') as fh:
                dump(self.data, fh)
        except Exception:
            print("Some problems!")


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


this_contacts_book = AddressBook()
this_notebook = Notebook()


action_commands = ["help", "add_record", "del_record", "edit_record", "show_birthdays", "add_note", "del_note", "edit_note_text", \
    "find_note", "show_note", "add_tag", "del_tag", "change_tag", "show_note_by_tag", "find_note_by_tag", "sort_files"]
exit_commands = ["good_bye", "close", "exit"]
commands_description = ["Returns the list of available CLI commands", "Adding the Record to the AddressBook", \
    "Deleting the Record", "Editing the Record", "Returns the list of Records with the birthdays within the requested period", \
        "Adding the Note to the Notebook", "Deleting the Note", "Editing the text of the Note", "Search for the Note", \
    "Displays the Note", "Adding the Tag to the Note", "Deleting the Tag", "Changing the Tag", "Returns the list of Notes by Tag", \
        "Searching the Note by Tag", "Sorting the files in a specified directory" , "Exits the program"]
commands_desc = [f"<<{cmd}>> - {desc}" for cmd, desc in zip(action_commands + [', '.join(exit_commands)], commands_description)]


def show_commands():
    for i in commands_desc:
        print(i)


ARCHIVES = {'.ZIP', '.GZ', '.TAR'}
AUDIO = {'.MP3', '.OGG', '.WAV', '.AMR'}
DOCUMENTS = {'.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX'}
IMAGES = {'.JPEG', '.PNG', '.JPG', '.SVG'}
VIDEO = {'.AVI', '.MP4', '.MOV', '.MKV'}


def folder_handling(folder: Path, file_list: dict):
    for file in folder.iterdir():
        if file.is_dir():
            file_list['folder'].append(file.name)
        else:
            if file.suffix.upper() in IMAGES:
                file_list['images'].append(file.name)
            elif file.suffix.upper() in VIDEO:
                file_list['video'].append(file.name)
            elif file.suffix.upper() in DOCUMENTS:
                file_list['documents'].append(file.name)
            elif file.suffix.upper() in AUDIO:
                file_list['audio'].append(file.name)
            elif file.suffix.upper() in ARCHIVES:
                file_list['archives'].append(file.name)
            else:
                file_list['unknown extensions'].append(file.name)


def sort_files(work_dir: str = None):

    file_list = {
        'images': [],
        'documents': [],
        'audio': [],
        'video': [],
        'archives': [],
        'unknown extensions': [],
        'folder': []
    }

    path = Path.cwd()
    if work_dir is not None:
        path = Path(work_dir)

    if path.exists() and path.is_dir:
        folder_handling(path, file_list)
        return output_file_list(file_list)
    else:
        return 'Путь к папке указан не корректно'


def output_file_list(file_list: dict):
    lenght = 120
    result = '=' * (lenght + 3) + '\n'
    result += str('|{:^20}|{:^100}|'.format('Category', 'File')) + '\n'
    result += '=' * (lenght + 3) + '\n'
    for category in file_list:
        for file in file_list[category]:
            result += str('|{:<20}|{:<100}|'.format(category, file)) + '\n'
        if len(file_list[category]) > 0:
            result += '=' * (lenght + 3) + '\n'
    return result


def input_error(func):
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except KeyError as error:
            result = str(error)
        except ValueError as error:
            result = str(error)
        except IndexError:
            result = "Incomplete command modifier. Give me name and phone please."
        return result
    return inner


def hello_handler(*args) -> str:
    return 'How can I help you?'


@input_error
def exit_handler(*args):
    this_notebook.save_data()
    this_contacts_book.save_book()
    raise SystemExit('Good bye!')


@input_error
def note_add_handler(argument: str) -> str:
    this_notebook.add_note(argument)
    return 'Record added to notebook'


@input_error
def note_del_handler(argument: str) -> str:
    this_notebook.del_note(argument)
    return 'Record deleted to from notebook'


@input_error
def note_edit_tag_handler(argument: str) -> str:
    this_notebook.edit_note_tag(argument)
    return ''


@input_error
def note_edit_handler(argument: str) -> str:
    this_notebook.edit_note_text(argument)
    return ''


@input_error
def note_find_by_tag_handler(argument: str) -> str:
    return this_notebook.find_note_by_tag(argument)


@input_error
def note_find_handler(argument: str) -> str:
    return this_notebook.find_note(argument)


@input_error
def note_show_by_tag_handler(argument: str) -> str:
    this_notebook.show_note_by_tag()
    return ''


@input_error
def note_show_handler(argument: str) -> str:
    this_notebook.show_note()
    return ''

# -------------------------------------------------


@input_error
def contact_add_handler(argument: str) -> str:
    this_contacts_book.add_record(Name(argument))
    contact_edit_handler(argument)
    return f'Added record {argument}'


@input_error
def contact_edit_handler(argument: str) -> str:
    this_contacts_book.edit_record(Name(argument))
    return ''


@input_error
def contact_del_handler(argument: str) -> str:
    this_contacts_book.del_record(Name(argument))
    return f'Deleted record {argument}'


@input_error
def contact_find_handler(argument: str) -> str:
    return this_contacts_book.find_record(argument)


@input_error
def contact_show_handler(*args) -> str:
    if len(this_contacts_book) == 0:
        return 'Phone book is empty'
    try:
        max_line = int(args[0])
    except ValueError:
        max_line = len(this_contacts_book)
    result = 'Phone book:\n'
    num_page = 0
    for page in this_contacts_book.iterator(max_line=max_line):
        num_page += 1
        result += f'<< page {num_page} >>\n' if max_line < len(this_contacts_book) else ''
        result += page
    return result


@input_error
def contact_birthday_handler(argument) -> str:
    return this_contacts_book.show_record_with_birthday(int(argument))


@input_error
def error_handler(*args):
    return "Type help command for information about other commands"


@input_error
def sort_file_handler(argument: str) -> str:
    return sort_files(argument)


@input_error
def help_handler(*args):
    show_commands()
    return ''


handlers: Dict[str, Callable] = {
    'hello': hello_handler,
    'close': exit_handler,
    'good bye': exit_handler,
    'exit': exit_handler,
    '.': exit_handler,

    'note add': note_add_handler,
    'note del': note_del_handler,
    'note edit tag': note_edit_tag_handler,
    'note edit': note_edit_handler,
    'note find by tag': note_find_by_tag_handler,
    'note find': note_find_handler,
    'note show by tag': note_show_by_tag_handler,
    'note show': note_show_handler,

    'contact add': contact_add_handler,
    'contact edit': contact_edit_handler,
    'contact del': contact_del_handler,
    'contact find': contact_find_handler,
    'contact show': contact_show_handler,

    'contact birthday': contact_birthday_handler,

    'error command': error_handler,

    'sort file': sort_file_handler,

    'help': help_handler
}


def string_parsing(user_input: str):
    user_input_list = user_input.split(' ')
    for command in handlers.keys():
        command_list = command.split(' ')
        if command == ' '.join(user_input_list[:len(command_list):]).lower():
            return command, ' '.join(user_input_list[len(command_list)::])

    return 'error command', None


def main():
    while True:
        input_user = input('Command: ')
        command, argument = string_parsing(input_user)
        function_handler = handlers.get(command)
        try:
            print(function_handler(argument))
        except SystemExit as e:
            print(e)
            break


if __name__ == '__main__':

    main()