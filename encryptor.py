import argparse
from ciphers import get_cipher
import hack as _hack
from sys import stdin
from sys import stdout
from contextlib import contextmanager

@contextmanager
def open_input(i):
    if i == None:
        yield stdin
    else:
        with open(i, "r") as input:
            yield input

@contextmanager
def open_output(i):
    if i == None:
        yield stdout
    else:
        with open(i, "w") as output:
            yield output

def encode(args):
    with open_input(args.input_file) as input:
        with open_output(args.output_file) as output:
            get_cipher(args.cipher).encode(input, output, args.key)

def decode(args):
    with open_input(args.input_file) as input:
        with open_output(args.output_file) as output:
            get_cipher(args.cipher).decode(input, output, args.key)

def train(args):
    with open_input(args.text_file) as text:
        with open_output(args.model_file) as model:
            _hack.train(text, model)

def hack(args):
    with open_input(args.input_file) as input:
        with open_output(args.output_file) as output:
            with open(args.model_file, 'r') as model:
                _hack.hack(input, output, model)

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()
encode_parser = subparsers.add_parser('encode')
encode_parser.add_argument("--cipher", type = str, choices = ['caesar', 'vigenere', 'vernam'], required = True)
encode_parser.add_argument("--key", required = True)
encode_parser.add_argument("--input-file", type = str)
encode_parser.add_argument("--output-file", type = str)
encode_parser.set_defaults(action = encode)

decode_parser = subparsers.add_parser('decode')
decode_parser.add_argument("--cipher", type = str, choices = ['caesar', 'vigenere', 'vernam'], required = True)
decode_parser.add_argument("--key", required = True)
decode_parser.add_argument("--input-file", type = str)
decode_parser.add_argument("--output-file", type = str)
decode_parser.set_defaults(action = decode)

train_parser = subparsers.add_parser('train')
train_parser.add_argument("--model-file", type = str, required = True)
train_parser.add_argument("--text-file", type = str)
train_parser.set_defaults(action = train)

hack_parser = subparsers.add_parser('hack')
hack_parser.add_argument("--model-file", type = str, required = True)
hack_parser.add_argument("--input-file", type = str)
hack_parser.add_argument("--output-file", type = str)
hack_parser.set_defaults(action = hack)

args = parser.parse_args()
args.action(args)
