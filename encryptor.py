import argparse
import caesar
import vigenere
import vernam
import hack
from sys import stdin
from sys import stdout

from string import ascii_lowercase as letters
letters_indexes = {letters[i] : i for i in range(len(letters))}

def name_support(f):
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

caesar.import_alphabet(letters, letters_indexes)
vigenere.import_alphabet(letters, letters_indexes)
vernam.import_alphabet(letters, letters_indexes)
hack.import_alphabet(letters, letters_indexes)

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()
encode_parser = subparsers.add_parser('encode')
encode_parser.add_argument("--cipher", type = str, choices = ['caesar', 'vigenere', 'vernam'], required = True)
encode_parser.add_argument("--key", required = True)
encode_parser.add_argument("--input-file", type = str)
encode_parser.add_argument("--output-file", type = str)
encode_parser.set_defaults(action = "encode")

decode_parser = subparsers.add_parser('decode')
decode_parser.add_argument("--cipher", type = str, choices = ['caesar', 'vigenere', 'vernam'], required = True)
decode_parser.add_argument("--key", required = True)
decode_parser.add_argument("--input-file", type = str)
decode_parser.add_argument("--output-file", type = str)
decode_parser.set_defaults(action = "decode")

train_parser = subparsers.add_parser('train')
train_parser.add_argument("--model-file", type = str, required = True)
train_parser.add_argument("--text-file", type = str)
train_parser.set_defaults(action = "train")

hack_parser = subparsers.add_parser('hack')
hack_parser.add_argument("--model-file", type = str, required = True)
hack_parser.add_argument("--input-file", type = str)
hack_parser.add_argument("--output-file", type = str)
hack_parser.set_defaults(action = "hack")

args = parser.parse_args()

if args.action == "encode":
    if args.cipher == "caesar":
        name_support(caesar.encode)(args.input_file, args.output_file, int(args.key))
    elif args.cipher == "vigenere":
        name_support(vigenere.encode)(args.input_file, args.output_file, str(args.key))
    elif args.cipher == "vernam":
        name_support(vernam.encode)(args.input_file, args.output_file, str(args.key))

if args.action == "decode":
    if args.cipher == "caesar":
        name_support(caesar.decode)(args.input_file, args.output_file, int(args.key))
    if args.cipher == "vigenere":
        name_support(vigenere.decode)(args.input_file, args.output_file, str(args.key))
    elif args.cipher == "vernam":
        name_support(vernam.decode)(args.input_file, args.output_file, str(args.key))

if args.action == "train":
    name_support(hack.train)(args.text_file, args.model_file)

if args.action == "hack":
    name_support(hack.hack)(args.input_file, args.output_file, args.model_file)
