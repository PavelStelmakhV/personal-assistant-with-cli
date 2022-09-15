from typing import Dict, Callable

from help_command import show_commands
from contact_book import *
from notebook import *
from sort import sort_files


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