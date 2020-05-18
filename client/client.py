import requests
import argparse
from contextlib import contextmanager
from sys import stdin, stdout


@contextmanager
def open_input(i):
    if i == '':
        print(' - Input:')
        yield stdin
    else:
        with open(i, 'r') as input:
            yield input


@contextmanager
def open_output(o):
    if o == '':
        print(' - Output:')
        yield stdout
    else:
        with open(o, 'w') as output:
            yield output


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


def input_command(main_args, input, method, command, args):
    with open_input(input) as i:
        args['input'] = i.read()
        return request_command(main_args, method, command, args)


def advanced_input(message, t):
    i = input(message)
    try:
       return t(i)
    except TypeError:
        return None


def info(main_args, object):
    if object not in {'model', 'alphabet'}:
        return f' Error# Unknown object \'{object}\'. Type \'help\' to get help'
    ID = advanced_input(f' Print {object} ID:  ', int)
    if ID is None:
        return ' Error# Incorrect ID'
    information = request_command(main_args, 'GET', f'get_{object}_information', dict(ID = ID))
    return f' ID {ID}: {information}'


def encrypt(main_args, action):
    if action == 'hack':
        ID = advanced_input(f' Print model ID:  ', int)
    else:
        ID = advanced_input(f' Print alphabet ID:  ', int)

    if ID is None:
        return ' Error# Incorrect ID'

    if action != 'hack':
        key = advanced_input(f' Print key:  ', str)
        if key is None:
            return ' Error# Incorrect key'

    i = input(f' Print name of the file to {action} (Tap Enter to read from console):  ')
    try:
        if action != 'hack':
            result = input_command(main_args, i, 'GET', action, dict(ID = ID, key = key))
        else:
            result = input_command(main_args, i, 'GET', action, dict(ID = ID))
    except FileNotFoundError:
        print(' Error# Input file not found')

    o = input(f' Print name of the file to save the result (Tap Enter to write to console):  ')
    try:
        with open_output(o) as out:
            out.write(result)
    except FileNotFoundError:
        print(' Error# Output file not found')


def add_alphabet(main_args):
    desc = str(input(' Print description of the alphabet:  '))
    i = input(' Print name of the alphabet file (Tap Enter to read from console):  ')
    try:
        result = input_command(main_args, i, 'POST', 'add_alphabet', dict(description = desc))
    except FileNotFoundError:
        return ' Error# Input file not found'
    if result == '':
        return ' Error# Incorrect alphabet. Alphabet should not contain same symbols'
    return f' Added with ID: {result}'


def add_model(main_args):
    ID = advanced_input(' Print ID of the model\'s alphabet:  ', int)
    if ID is None:
        return ' Error# Incorrect ID'

    desc = str(input(' Print description of the model:  '))
    i = input(' Print name of the model file (Tap Enter to read from console):  ')
    try:
        result = input_command(main_args, i, 'POST', 'add_model', dict(description = desc, ID = ID))
    except FileNotFoundError:
        return ' Error# Input file not found'
    if result == '':
        return ' Error# Alphabet not found'
    return f' Added with ID: {result}'


def add(main_args, object):
    if object == 'alphabet':
        return add_alphabet(main_args)
    elif object == 'model':
        return add_model(main_args)
    else:
        return f' Error# Unknown object \'{object}\'. Type \'help\' to get help'


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
