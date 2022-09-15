from handlers import handlers
from parcer import string_parsing


def main():
    while True:
        input_user = input('Command: ')
        command, argument = string_parsing(input_user)
        function_handler = handlers.get(command)
        try:
            print(function_handler(argument))
        except SystemExit as e:
            print(e)
            break


if __name__ == '__main__':

    main()
