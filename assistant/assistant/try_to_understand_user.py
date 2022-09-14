def try_to_understand_user(user_input):
    assistant_commands = ('days_to_birthday', 'save', 'search', 'open', 'iterator', 'add', 'hello',
                          'change', 'phone', 'show_all')
    s = ''
    if user_input[0] == '':
        s += 'string cannot be empty'
    elif user_input[0] == 'days_to_birthday':
        if len(user_input) == 1:
            s += 'operator days_to_birthday error: birthday was missed'
        elif len(user_input) > 2:
            s += 'operator days_to_birthday error: too much args'

    elif user_input[0] == 'save':
        if len(user_input) == 1:
            s += 'operator save error: file name was missed'
        elif len(user_input) > 2:
            s += 'operator save error: too much args'

    elif user_input[0] == 'search':
        if len(user_input) == 1:
            s += 'operator search error: key word was missed'
        elif len(user_input) > 2:
            s += 'operator search error: too much args'

    elif user_input[0] == 'open':
        if len(user_input) == 1:
            s += 'operator open error: file name was missed'
        elif len(user_input) > 2:
            s += 'operator open error: too much args'

    elif user_input[0] == 'iterator':
        if len(user_input) == 1:
            s += 'operator iterator error: amount_of_elements was missed'
        elif len(user_input) > 2:
            s += 'operator iterator error: too much args'
    elif user_input[0] == 'add':
        if len(user_input) < 3:
            s += 'operator add error: name or phone number were missed'
        elif len(user_input) > 4:
            s += 'operator add error: too much args'
    elif user_input[0] == 'hello' and len(user_input) > 1:
        s += 'operator hello error: hello must be a single operator'
    elif user_input[0] == 'change':
        if len(user_input) < 3:
            s += 'operator change error: name or phone number were missed'
        elif len(user_input) > 3:
            s += 'operator change error: too much args'
    elif user_input[0] == 'phone':
        if len(user_input) < 2:
            s += 'operator phone error: name was missed'
        elif len(user_input) > 2:
            s += 'operator phone error: too much args'
    elif user_input[0] == 'show' and user_input[1] == 'all':
        if len(user_input) > 2:
            s += 'operator show all error: show all must be a single operator'

    s += '\nmaybe you mean : '
    for command in assistant_commands:
        if (user_input[0] in command or command in user_input[0] or user_input[0][0:2] in command
            or user_input[0][0:3] in command) and user_input[0] != command:
            s += command + ' '
    return s


print(try_to_understand_user(['search']))
