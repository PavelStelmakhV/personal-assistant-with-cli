from typing import Dict, Callable


def input_error(func):
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except KeyError as error:
            result = str(error) + '\nTry again.'
        except ValueError as error:
            result = str(error) + '\nTry again.'
        except IndexError:
            result = "Incomplete command modifier. Give me name and phone please." + '\nTry again.'
        return result
    return inner


def handler_hello(*args) -> str:
    return 'How can I help you?'


@input_error
def handler_exit(*args):
    raise SystemExit('Good bye!')


handlers: Dict[str, Callable] = {
    'hello': handler_hello,
    'close': handler_exit,
    'good bye': handler_exit,
    'exit': handler_exit,
    '.': handler_exit
}