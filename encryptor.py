import argparse as _argparse
import caesar as _caesar
import vigenere as _vigenere

_parser = _argparse.ArgumentParser()
_parser.add_argument("action", type = str, choices = ["encode", "decode", "train", "hack"])
_parser.add_argument("--cipher", type = str, choices = ['caesar', 'vigenere'])
_parser.add_argument("--key")
_parser.add_argument("--input-file", type = str)
_parser.add_argument("--output-file", type = str)
_parser.add_argument("--text-file", type = str)
_parser.add_argument("--model-file", type = str)
args = _parser.parse_args()

if args.action == "encode":
    if args.cipher == "caesar":
        _caesar.encode(args.key, args.input_file, args.output_file)
    elif args.cipher == "vigenere":
        _vigenere.encode(args.key, args.input_file, args.output_file)

if args.action == "decode":
    if args.cipher == "caesar":
        _caesar.decode(args.key, args.input_file, args.output_file)
    if args.cipher == "vigenere":
        _vigenere.decode(args.key, args.input_file, args.output_file)

if args.action == "train":
    _caesar.train(args.text_file, args.model_file)

if args.action == "hack":
    if args.cipher == "caesar":
        _caesar.hack(args.input_file, args.output_file, args.model_file)
    if args.cipher == "vigenere":
        _vigenere.hack(args.input_file, args.output_file, args.model_file)
