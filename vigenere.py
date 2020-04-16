from sys import stdout
from sys import stdin
from string import ascii_lowercase as letters
letters_indexes = {letters[i] : i for i in range(len(letters))}

def get_name_supporing_function(f):
    def name_supporing_function(*args):
        if args[0] == None:
            if args[1] == None:
                f(stdin, stdout, *args[2:])
            else:
                with open(args[1], 'w') as output:
                    f(stdin, output, *args[2:])
        else:
            if args[1] == None:
                with open(args[0], 'r') as input:
                    f(input, stdout, *args[2:])
            else:
                with open(args[0], 'r') as input:
                    with open(args[1], 'w') as output:
                        f(input, output, *args[2:])
    return name_supporing_function

def encode_symbol(key, s):
    if not s.isalpha():
        return s
    elif s.islower():
        return letters[(letters_indexes[s] + key) % len(letters)]
    else:
        return letters[(letters_indexes[s.lower()] + key) % len(letters)].upper()

def stream_encode(input, output, key):
    index = 0
    while True:
        try:
            s = input.read(1)
        except:
            break
        if s == "":
            break
        output.write(encode_symbol(letters_indexes[key[index].lower()], s))
        index = (index + 1) % len(key)

def stream_decode(input, output, key):
    index = 0
    while True:
        try:
            s = input.read(1)
        except:
            break
        if s == "":
            break
        output.write(encode_symbol(-letters_indexes[key[index].lower()], s))
        index = (index + 1) % len(key)

decode = get_name_supporing_function(stream_decode)

encode = get_name_supporing_function(stream_encode)
