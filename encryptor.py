import argparse
import caesar
import vigenere

parser = argparse.ArgumentParser()
parser.add_argument("action", type = str, choices = ["encode", "decode", "train", "hack"])
parser.add_argument("--cipher", type = str, choices = ['caesar', 'vigenere'])
parser.add_argument("--key")
parser.add_argument("--input-file", type = str)
parser.add_argument("--output-file", type = str)
parser.add_argument("--text-file", type = str)
parser.add_argument("--model-file", type = str)
args = parser.parse_args()

if args.action == "encode":
    if args.cipher == "caesar":
        caesar.encode(args.input_file, args.output_file, args.key)
    elif args.cipher == "vigenere":
        vigenere.encode(args.input_file, args.output_file, args.key)

if args.action == "decode":
    if args.cipher == "caesar":
        caesar.decode(args.input_file, args.output_file, args.key)
    if args.cipher == "vigenere":
        vigenere.decode(args.input_file, args.output_file, args.key)

if args.action == "train":
    caesar.train(args.text_file, args.model_file)

if args.action == "hack":
    if args.cipher == "caesar":
        caesar.hack(args.input_file, args.output_file, args.model_file)
    if args.cipher == "vigenere":
        vigenere.hack(args.input_file, args.output_file, args.model_file)
