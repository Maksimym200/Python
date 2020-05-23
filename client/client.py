import requests
import argparse
from contextlib import contextmanager
from sys import stdin, stdout
from strings import methods, errors, messages, objects


@contextmanager
def open_stream(stream, mode):
    if not stream:
        args = (messages._in, stdin) if mode == 'r' else (messages._out, stdout) if mode == 'w' else None
        print(args[0])
        yield args[1]
    else:
        with open(stream, mode) as file_stream:
            yield file_stream


def create_main_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host')
    parser.add_argument('--port', type=int)
    return parser


def request_command(main_args, method, command, args):
    address = messages.address(main_args, command)
    if method == 'GET':
        return requests.get(address, params = args).text
    if method == 'POST':
        return requests.post(address, params = args).text


def input_command(main_args, file_input, method, command, args):
    with open_stream(file_input, 'r') as istream:
        args['input'] = istream.read()
        return request_command(main_args, method, command, args)


def advanced_input(message, input_type):
    file_input = input(message)
    try:
       return input_type(file_input)
    except ValueError:
        return None


def info(main_args, obj):
    if obj not in objects.server_objects:
        print(errors.unknown_object(obj))
        print(messages.suggest_help)
        return
    ID = advanced_input(messages.print_message(obj, objects.ID), int)
    if ID is None:
        print(errors.incorrect_ID)
        return
    information = request_command(main_args, 'GET', methods.getinfo(obj), dict(ID = ID))
    print(information)


def encrypt(main_args, action):
    ID = advanced_input(messages.print_message(objects.model if \
        action == objects.hack else objects.alphabet, objects.ID), int)
    if ID is None:
        print(errors.incorrect_ID)
        return

    if action != objects.hack:
        key = input(messages.print_message(objects.key, None))

    file_input = input(messages.print_input_file(action))
    try:
        if action != objects.hack:
            result = input_command(main_args, file_input, 'GET', methods.action(action), dict(ID = ID, key = key))
        else:
            result = input_command(main_args, file_input, 'GET', methods.action(action), dict(ID = ID))
    except FileNotFoundError:
        print(errors.no_file_input)
        return

    file_output = input(messages.print_output_file)
    try:
        with open_stream(file_output, 'w') as ostream:
            ostream.write(result)
    except FileNotFoundError:
        print(errors.no_file_output)
        return


def add(main_args, obj):
    ID = 0
    if obj == objects.model:
        ID = advanced_input(messages.print_message(objects.alphabet, objects.ID), int)
        if ID is None:
            print(errors.incorrect_ID)
            return

    desc = input(messages.print_message(obj, objects.description))
    file_input = input(messages.print_object_file(obj))
    try:
        result = input_command(main_args, file_input, 'POST', methods.add(obj), dict(description = desc, ID = ID))
    except FileNotFoundError:
        print(errors.no_file_input)
        return
    print(messages.added(result) if result.isdigit else result)


def try_exit():
    while True:
        answer = input(messages.leave)
        if answer == 'y':
            exit()
        elif answer == 'n':
            break
        print()


def main():
    main_parser = create_main_parser()
    main_args = main_parser.parse_args()
    while True:
        try:
            command = input(messages.enter_command).split(' ')
            if command[0] == 'info' and len(command) > 1:
                info(main_args, command[1])
            elif command[0] == 'add' and len(command) > 1:
                add(main_args, command[1])
            elif command[0] in objects.encrypt_commands:
                encrypt(main_args, command[0])
            elif command[0] == 'help':
                print(messages.help)
            elif command[0] == 'exit':
                try_exit()
            else:
                print(errors.unknown_command(command[0]))
                print(messages.suggest_help)
        except KeyboardInterrupt:
            print()
            try_exit()
        print()


if __name__ == '__main__':
    try:
        main()
    except requests.exceptions.ConnectionError:
        print(errors.no_server)
