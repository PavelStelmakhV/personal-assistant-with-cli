from handlers import handlers


def string_parsing(user_input: str):
    user_input_list = user_input.split(' ')
    for command in handlers.keys():
        command_list = command.split(' ')
        if command == ' '.join(user_input_list[:len(command_list):]).lower():
            return command, ' '.join(user_input_list[len(command_list)::])

    return 'error command', None