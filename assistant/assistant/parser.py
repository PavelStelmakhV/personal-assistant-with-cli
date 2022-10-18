from typing import List
from assistant.decorators import *


class Parsers:

    __commands: List[str] = [
        'hello',
        'close',
        'good bye',
        'exit',

        'note add',
        'note del',
        'note edit tag',
        'note edit',
        'note find by tag',
        'note find',
        'note show by tag',
        'note show',

        'contact add',
        'contact edit',
        'contact del',
        'contact find',
        'contact show',

        'contact birthday',

        'sort file',
        'help'
    ]

    @parser_handler
    def parse_user_input(self, user_input: str) -> tuple[str, str]:
        user_input_list = user_input.split(' ')
        for command in self.__commands:
            command_list = command.split(' ')
            if command == ' '.join(user_input_list[:len(command_list):]).lower():
                parser = getattr(self, '_' + command.replace(' ', '_'))
                return parser(' '.join(user_input_list[len(command_list)::]))

        raise ValueError("Unknown command!")

    def _hello(self, user_input: str):
        return 'hello', ''

    def _close(self, user_input: str):
        return 'exit', ''

    def _good_bye(self, user_input: str):
        return 'exit', ''

    def _exit(self, user_input: str):
        return 'exit', ''
    #--------------- N O T E --------------------
    def _note_add(self, note_name: str):
        if note_name == '':
            raise ValueError("Bad input")
        else:
            return "note add", note_name

    def _note_del(self, note_name: str):
        if note_name == '':
            raise ValueError("Bad input")
        else:
            return "note del", note_name

    def _note_edit_tag(self, note_name: str):
        if note_name == '':
            raise ValueError("Bad input")
        else:
            return "note edit tag", note_name

    def _note_edit(self, note_name: str):
        if note_name == '':
            raise ValueError("Bad input")
        else:
            return "note edit", note_name

    def _note_find_by_tag(self, user_input: str):
        return "note find by tag", user_input

    def _note_find(self, user_input: str):
        return "note find", user_input

    def _note_show_by_tag(self, user_input: str):
        return "note show by tag", user_input

    def _note_show(self, user_input: str):
        return "note show", []
    #-------------- C O N T A C T ---------------------
    def _contact_add(self, username: str):
        if username == '':
            raise ValueError("Bad input")
        else:
            return "contact add", username

    def _contact_edit(self, username: str):
        if username == '':
            raise ValueError("Bad input")
        else:
            return "contact edit", username

    def _contact_del(self, username: str):
        if username == '':
            raise ValueError("Bad input")
        else:
            return "contact del", username

    def _contact_find(self, username: str):
        if username == '':
            raise ValueError("Bad input")
        else:
            return "contact find", username

    def _contact_show(self, user_input: str):
        return "contact show", ''

    def _contact_birthday(self, user_input: str):
        return "contact birthday", user_input

    def _sort_file(self, user_input: str):
        return "sort file", user_input

    def _help(self, user_input: str):
        return "help", []