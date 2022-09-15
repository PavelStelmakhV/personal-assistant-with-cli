import math
from datetime import datetime
from collections import UserDict


class Field:
    pass


class Name:
    value = ''

    def delete(self):
        self.value = ''

    def edit(self, text_to_edit):
        self.value = text_to_edit

    def add(self, user_name):
        self.value = user_name


class Phone:
    value = ''
    dict_operator = ('096', '097', '098', '063', '067', '093', '050', '095', '066')

    def validate_phone(self, user_phone):
        if 9 < len(user_phone) < 14:
            if (user_phone[0:2] == '+38' and user_phone[3:5] in self.dict_operator) or \
                    (user_phone[0:2] in self.dict_operator):
                return user_phone

        return 'None'

    def add(self, user_phone):
        self.value = self.validate_phone(user_phone)

    def delete(self):
        self.value = ''

    def edit(self, text_to_edit):
        self.value = self.validate_phone(text_to_edit)


class Birthday:
    value = ''

    def validate(self, datetime_value):
        if (0 < int(datetime_value[0]) < 32) \
                and (0 < int(datetime_value[1]) < 13) \
                and (1900 < int(datetime_value[2]) < 2023):
            return True
        else:
            return False

    def add(self, birthday):
        self.value = birthday
        self.date_value = birthday.split('.')

        if self.validate(self.date_value):
            self.datetime_value = datetime(day=int(self.date_value[0]), month=int(self.date_value[1]),
                                           year=int(self.date_value[2]))
        else:
            self.datetime_value = datetime(day=1, month=1, year=1)
            self.value = ''

    def delete(self):
        self.value = ''

    def edit(self, text_to_edit):
        self.value = text_to_edit


class Address:
    value = ''

    def add(self, user_address):
        self.value = user_address

    def delete(self):
        self.value = ''

    def edit(self, text_to_edit):
        self.value = text_to_edit


class Email:
    value = ''
    email_box_names = ('gmail.com', 'ukr.net', 'yahoo.com', 'hotmail.com')

    def validate_email(self, user_email):
        user_name, email_box = user_email.split('@')
        if (5 < len(user_name) < 50) and (email_box in self.email_box_names):
            return user_email
        return 'None'

    def add(self, user_email):
        self.value = self.validate_email(user_email)

    def delete(self):
        self.value = ''

    def edit(self, text_to_edit):
        self.value = self.validate_email(text_to_edit)


class Record(Field, Name, Phone, Birthday, Address, Email):
    def Add(self, user_name, user_phone='', user_birthday='', user_address='', user_email=''):
        self.name = Name()
        self.name.add(user_name)

        self.phone = Phone()

        if user_phone != '':
            self.phone.add(user_phone)
        else:
            self.phone.add("Empty")

        if user_birthday != '':
            self.birthday = Birthday()
            self.birthday.add(user_birthday)

        if user_address != '':
            self.address = Address()
            self.address.add(user_address)

        if user_email != '':
            self.email = Email()
            self.email.add(user_email)

    def Delete(self):
        self.phone.value = ''

    def Edit(self, new_phone):
        self.phone.value = new_phone

    def days_to_birthday(self):
        today_date = datetime.now()
        difference = today_date - self.birthday.datetime_value
        print(f'days to birthday: {int(math.fabs(difference.days))}')


class AddressBook(UserDict, Record):
    dict = {}

    def find_by_name(self, name):
        print(f'name: {name}')
        print(f'\t {self.dict[name].phone.value}')

    def find_by_phone(self, phone):
        for key, value in self.dict.items():
            if value.phone.value == phone:
                print(f'{key}:{phone}')

    def edit_email(self, user_name, new_email):
        self.dict[user_name].email.edit(new_email)

    def edit_name(self, user_name, new_name):
        self.dict[user_name].name.edit(new_name)

    def edit_phone(self, user_name, new_phone):
        self.dict[user_name].phone.edit(new_phone)

    def edit_address(self, user_name, new_address):
        self.dict[user_name].address.edit(new_address)

    def edit_birthday(self, user_name, new_birthday):
        self.dict[user_name].birthday.edit(new_birthday)

    def delete_email(self, user_name):
        self.dict[user_name].email.delete()

    def delete_name(self, user_name):
        self.dict[user_name].name.delete()

    def delete_phone(self, user_name):
        self.dict[user_name].phone.delete()

    def delete_address(self, user_name):
        self.dict[user_name].address.delete()

    def delete_birthday(self, user_name):
        self.dict[user_name].birthday.delete()


this_phonebook = AddressBook()