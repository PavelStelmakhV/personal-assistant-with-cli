from collections import UserDict
from datetime import datetime, timedelta
from pickle import load, dump
from pathlib import Path


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


this_contacts_book = AddressBook()


