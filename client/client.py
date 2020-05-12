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

def check_type(type, obj):
    try:
       type(obj)
    except ValueError:
        return False
    return True

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

def info(main_args, object):
    ID = input(f' Print {object} ID:  ')
    if not check_type(int, ID):
        print(' Error# Incorrect ID')
        return
    ID = int(ID)
    help = request_command(main_args, 'GET', f'get_{object}_information', dict(ID = ID))
    return f' ID {ID}: {help}'

def encode(main_args, shift = 'encode'):
    ID = input(f' Print alphabet ID:  ')
    if not check_type(int, ID):
        print(' Error# Incorrect ID')
        return
    ID = int(ID)

    key = input(f' Print key:  ')
    if not check_type(str, ID):
        print(' Error# Incorrect Key')
        return
    key = str(key)

    i = input(f' Print name of the file to {shift} (Tap Enter to read from console):  ')
    try:
        result = input_command(main_args, i, 'GET', shift, dict(ID = ID, key = key))
    except FileNotFoundError:
        print(' Error# Input file not found')

    o = input(f' Print name of the file to save the result (Tap Enter to write to console):  ')
    try:
        with open_output(o) as out:
            out.write(result)
    except FileNotFoundError:
        print(' Error# Output file not found')

def hack(main_args):
    ID = input(f' Print model ID:  ')
    try:
        ID = int(ID)
    except ValueError:
        print(' Error# Incorrect ID')
        return
    i = input(f' Print name of the file to hack (Tap Enter to read from console):  ')
    try:
        result = input_command(main_args, i, 'GET', 'hack', dict(ID = ID))
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
    ID = input(' Print ID of the model\'s alphabet:  ')
    if not check_type(int, ID):
        print(' Error# Incorrect ID')
        return
    ID = int(ID)
    desc = str(input(' Print description of the model:  '))
    i = input(' Print name of the model file (Tap Enter to read from console):  ')
    try:
        result = input_command(main_args, i, 'POST', 'add_model', dict(description = desc, ID = ID))
    except FileNotFoundError:
        return ' Error# Input file not found'
    if result == '':
        return ' Error# Alphabet not found'
    return f' Added with ID: {result}'

def help():
    print(' Available commands: ')
    print(' - info {alphabet / model} : get alphabet or model information')
    print(' - add {alphabet / model} : add alphabet or model')
    print(' - encode : encode text with vigenere cipher')
    print(' - decode : decode text with vigenere cipher')
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
            command = input('\n Enter command:  ')
            if command == 'info alphabet':
                print(info(main_args, 'alphabet'))
            elif command == 'info model':
                print(info(main_args, 'model'))
            elif command == 'add alphabet':
                print(add_alphabet(main_args))
            elif command == 'add model':
                print(add_model(main_args))
            elif command == 'encode':
                encode(main_args)
            elif command == 'decode':
                encode(main_args, 'decode')
            elif command == 'hack':
                hack(main_args)
            elif command == 'help':
                help()
            elif command == 'exit':
                try_exit()
            else:
                print(f' Unknown command \'{command}\'. Type \'help\' to get help')
        except KeyboardInterrupt:
            print('')
            try_exit()

if __name__ == '__main__':
    try:
        main()
    except requests.exceptions.ConnectionError:
        print(' #Error Server not found')
