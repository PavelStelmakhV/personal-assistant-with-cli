from typing import Dict, Callable
from assistant import contact_book
import contact_book
import note_book
import help
from sort import SortFolder
from parcer import Parsers
from decorators import *

from typing import Set


class InputOutput:
    def __init__(self):
        self.contactbook: contact_book.AddressBook = None
        self.notebook: note_book.Notebook = None
        self._sortfolder = SortFolder()
        self._parsers = Parsers()

    def hello_handler(self, *args) -> str:
        return 'How can I help you?'

    @command_handler
    def exit_handler(self, *args):
        raise SystemExit('Good bye!')

    @command_handler
    def note_add_handler(self, argument: str) -> str:
        input_text = input('Input text note:')
        return self.notebook.add_note(argument, input_text)

    @command_handler
    def note_del_handler(self, argument: str) -> str:
        return self.notebook.del_note(argument)

    @command_handler
    def note_edit_tag_handler(self, argument: str) -> str:
        self.notebook.edit_note_tag(argument)
        flag = input('input add or delete tag (a/d)')
        if flag == 'a':
            tag = input('input new tag: ')
            return self.notebook.edit_note_tag_add(argument, tag)
        else:
            tag = input('input remove tag: ')
            return self.notebook.edit_note_tag_del(argument, tag)
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    @command_handler
    def note_edit_handler(self, name_note: str) -> str:
        print(self.notebook[name_note])
        text_note = input('>')
        flag = input('input add or overwrite text (a/o)')
        if flag == 'a':
            add_text = True
        elif flag == 'o':
            add_text = False
        return self.notebook.edit_note_text(name_note, text_note, add_text)

    @command_handler
    def note_find_by_tag_handler(self, argument: str) -> str:
        return self.notebook.find_note_by_tag(argument)

    @command_handler
    def note_find_handler(self, argument: str) -> str:
        return self.notebook.find_note(argument)

    @command_handler
    def note_show_by_tag_handler(self, argument: str) -> str:
        return self.notebook.show_note_by_tag()

    @command_handler
    def note_show_handler(self, argument: str) -> str:
        return self.notebook.show_note()
    # -------------------------------------------------
    @command_handler
    def contact_add_handler(self, argument: str) -> str:
        result = []
        self.contactbook.add_record(contact_book.Name(argument))

        result.append(f'Added record {argument}.')
        result.append(self._add_phone(argument))
        result.append(self._add_address(argument))
        result.append(self._add_email(argument))
        result.append(self._add_birthday(argument))
        self.contactbook.save_book()
        return ' '.join(result)


    @command_handler
    def contact_edit_handler(self, argument: str) -> str:
        self.contactbook.edit_record(contact_book.Name(argument))

        print('1. Add phone\n2. Delete phone\n3. Change phone\n4. Change address\n5. Change E-mail\n6. Change birthday')
        num_choose = input('Choose a number: ')
        operation_with_record =['_add_phone', '_del_phone', '_change_phone', '_add_address', '_add_email', '_add_birthday']
        print(operation_with_record[int(num_choose)-1])
        command_function = getattr(self, operation_with_record[int(num_choose)-1])
        result = command_function(argument)
        self.contactbook.save_book()
        return f'Edited record {argument}. {result}'
    #--------------------------------------------
    @command_handler
    def _add_phone(self, argument: str) -> str:
        num_phone = input('Input phone: ')
        if num_phone is not None:
            return self.contactbook[contact_book.Name(argument).value].add_phone(contact_book.Phone(num_phone))

    @command_handler
    def _del_phone(self, argument: str) -> str:
        num_phone = input('Enter phone number to delete: ')
        return self.contactbook[contact_book.Name(argument).value].delete_phone(contact_book.Phone(num_phone))

    @command_handler
    def _change_phone(self, argument: str) -> str:
        change_phone = input('Enter phone number to change: ')
        new_phone = input('Enter new phone: ')
        return self.contactbook[contact_book.Name(argument).value].change_phone(contact_book.Phone(change_phone), contact_book.Phone(new_phone))

    @command_handler
    def _add_address(self, argument: str) -> str:
        address = input('Input address: ')
        if address is not None:
            return self.contactbook[contact_book.Name(argument).value].set_address(contact_book.Address(address))

    @command_handler
    def _add_email(self, argument: str) -> str:
        email = input('Input email: ')
        if email is not None:
            return self.contactbook[contact_book.Name(argument).value].set_email(contact_book.Email(email))

    @command_handler
    def _add_birthday(self, argument: str) -> str:
        birthday = input('Input birthday: ')
        if birthday is not None:
            return self.contactbook[contact_book.Name(argument).value].set_birthday(contact_book.Birthday(birthday))
    #------------------------------------------------------------

    @command_handler
    def contact_del_handler(self, argument: str) -> str:
        self.contactbook.del_record(contact_book.Name(argument))
        self.contactbook.save_book()
        return f'Deleted record {argument}'


    @command_handler
    def contact_find_handler(self, argument: str) -> str:
        return self.contactbook.find_record(argument)


    @command_handler
    def contact_show_handler(self, *args) -> str:
        if len(self.contactbook) == 0:
            return 'Phone book is empty'
        try:
            max_line = int(args[0])
        except ValueError:
            max_line = len(self.contactbook)
        result = 'Phone book:\n'
        num_page = 0
        for page in self.contactbook.iterator(max_line=max_line):
            num_page += 1
            result += f'<< page {num_page} >>\n' if max_line < len(self.contactbook) else ''
            result += page
        return result

    @command_handler
    def contact_birthday_handler(self, argument) -> str:
        return self.contactbook.show_record_with_birthday(int(argument))

    @command_handler
    def sort_file_handler(self, argument: str) -> str:
        return self._sortfolder.sort_files(argument)

    @command_handler
    def help_handler(self, *args):
        return help.show_commands()

    def setup_phonebook(self, phonebook):
        self.contactbook = phonebook

    def setup_notebook(self, notebook):
        self.notebook = notebook

    def loop_input_putput(self, command_line:str='Command', pre_command: str=''):
        while True:
            user_input = input(f'{command_line}: ')

            result = self._parsers.parse_user_input(user_input=user_input)
            if len(result) != 2:
                print(result)
                continue
            command, argument = result
            command_function = getattr(self, command.replace(" ", "_") + "_handler")

            try:
                command_response = command_function(argument)
                print(command_response)
            except SystemExit as e:
                print(str(e))
                break

    def run(self):

        with contact_book.AddressBook() as phonebook:
            self.setup_phonebook(phonebook)
            with note_book.Notebook() as notebook:
                self.setup_notebook(notebook)
                self.loop_input_putput()


def main():

    input_output = InputOutput()
    input_output.run()


if __name__ == '__main__':

    main()
