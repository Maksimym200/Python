import requests
import argparse
from contextlib import contextmanager
from sys import stdin, stdout


@contextmanager
def open_stream(stream, mode):
    if not stream:
        args = ('Input', stdin) if mode == 'r' else ('Output', stdout) if mode == 'w' else None
        print(f' - {args[0]}:')
        yield args[1]
    else:
        with open(stream, mode) as file_stream:
            yield file_stream


def create_main_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', default=8888, type=int)
    return parser


def request_command(main_args, method, command, args):
    address = f'http://{main_args.host}:{main_args.port}/{command}'
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
    except TypeError:
        return None


def info(main_args, obj):
    if obj not in {'model', 'alphabet'}:
        return f' Error# Unknown object \'{obj}\'. Type \'help\' to get help'
    ID = advanced_input(f' Print {obj} ID:  ', int)
    if ID is None:
        return ' Error# Incorrect ID'
    information = request_command(main_args, 'GET', f'get_{obj}_information', dict(ID = ID))
    return f' ID {ID}: {information}'


def encrypt(main_args, action):
    ID = advanced_input(f' Print {"model" if action == "hack" else "alphabet"} ID:  ', int)
    if ID is None:
        return ' Error# Incorrect ID'

    if action != 'hack':
        key = advanced_input(f' Print key:  ', str)
        if key is None:
            return ' Error# Incorrect key'

    file_input = input(f' Print name of the file to {action} (Tap Enter to read from console):  ')
    try:
        if action != 'hack':
            result = input_command(main_args, file_input, 'GET', action, dict(ID = ID, key = key))
        else:
            result = input_command(main_args, file_input, 'GET', action, dict(ID = ID))
    except FileNotFoundError:
        print(' Error# Input file not found')

    file_output = input(f' Print name of the file to save the result (Tap Enter to write to console):  ')
    try:
        with open_stream(file_output, 'w') as ostream:
            ostream.write(result)
    except FileNotFoundError:
        print(' Error# Output file not found')


def add(main_args, obj):
    ID = 0
    if obj == 'model':
        ID = advanced_input(' Print ID of the model\'s alphabet:  ', int)
        if ID is None:
            return ' Error# Incorrect ID'

    desc = str(input(f' Print description of the {obj}:  '))
    file_input = input(f' Print name of the {obj} file (Tap Enter to read from console):  ')
    try:
        result = input_command(main_args, file_input, 'POST', f'add_{obj}', dict(description = desc, ID = ID))
    except FileNotFoundError:
        return ' Error# Input file not found'
    if result == '':
        return ' Error# Incorrect alphabet. Alphabet should not contain same symbols' \
            if obj == 'alphabet' else ' Error# Alphabet not found'
    return f' Added with ID: {result}'


def help():
    print(' Available commands: ')
    print(' - info {alphabet / model} : get alphabet or model information')
    print(' - add {alphabet / model} : add alphabet or model')
    print(' - encode : encode text with vigenere cipher')
    print(' - decode : decode input with vigenere cipher')
    print(' - hack : hack encoded text')
    print(' - exit : exit the program')


def try_exit():
    while True:
        answer = input(' Are you sure you want to leave (y/n)?  ')
        if answer == 'y':
            print(' Thanks for using this soft!')
            print(' If you want to help in the development of this project, please donate!')
            exit()
        elif answer == 'n':
            print(' Canceled')
            break
        else:
            print(' Error# Incorrect input')


def main():
    main_parser = create_main_parser()
    main_args = main_parser.parse_args()
    while True:
        try:
            command = input('\n Enter command:  ').split(' ')
            if command[0] == 'info' and len(command) > 1:
                print(info(main_args, command[1]))
            elif command[0] == 'add' and len(command) > 1:
                print(add(main_args, command[1]))
            elif command[0] in {'encode', 'decode', 'hack'}:
                encrypt(main_args, command[0])
            elif command[0] == 'help':
                help()
            elif command[0] == 'exit':
                try_exit()
            else:
                print(f' Error# Unknown command \'{command[0]}\'. Type \'help\' to get help')
        except KeyboardInterrupt:
            print()
            try_exit()


if __name__ == '__main__':
    try:
        main()
    except requests.exceptions.ConnectionError:
        print(' #Error Server not found')
                        
