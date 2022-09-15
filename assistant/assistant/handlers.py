from typing import Dict, Callable
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
    # this_notebook.del_note(argument)
    # return 'Record deleted to from notebook'


@input_error
def error_handler(*args):
    return "Type help command for information about other commands"


@input_error
def sort_file_handler(argument: str) -> str:
    return sort_files(argument)


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
    'error command': error_handler,
    'sort file': sort_file_handler
}