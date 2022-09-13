from datetime import datetime, timedelta

def show_birthdays(self, n_days = None): 
        bdays_count_list = list(filter(lambda item: item.birthday.value, [i for i in self.data.values()]))
        if bdays_count_list:
            try: 
                n = input(f"Please enter the number of days within which you want to find the Records with birthdays: ").lower().strip()
                if n.isdigit():
                    n_days = int(n)
                else:
                    raise ValueError          
            except ValueError:
                print(f"The number of days was not properly set.")
                return None
            bdays_list = [] 
            current_date = datetime.today()
            search_period = (current_date+timedelta(days=n_days)).date()
            for record in self.data.values():
                if record.birthday.value:
                    if search_period.year > current_date.year:
                        bday_date = datetime.strptime(record.birthday.value[:6] + str(current_date.year+1), '%d.%m.%Y').date()
                        if current_date.date() < bday_date <= search_period:
                            bdays_list.append(record)
                    bday_date = datetime.strptime(record.birthday.value[:6] + str(current_date.year), '%d.%m.%Y').date()
                    if current_date.date() < bday_date <= search_period:
                        bdays_list.append(record)
            if bdays_list:
                print([str(_) for _ in bdays_list])
            else:
                print("No Records with birthdays within the requested period found")
        else:
            print("There are no Records with dates of birth in the AddressBook")

