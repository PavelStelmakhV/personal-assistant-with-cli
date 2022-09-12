import math
from datetime import datetime
#11111

class Field:
    pass


class Name:
    value = ''

    def add(self, user_name):
        self.value = user_name


class Phone:
    value = ''

    def validate_phone(self, user_phone):
        if len(user_phone) > 9 and len(user_phone) < 15:
            return user_phone
        else:
            return 'None'

    def add(self, user_phone):
        self.value = self.validate_phone(user_phone)


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


class Address:
    value = ''

    def add(self, user_address):
        self.value = user_address


class Email:
    value = ''

    def add(self, user_email):
        self.value = user_email


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
