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

    def add(self, birthday):
        self.value = birthday
        self.date_value = birthday.split('.')
