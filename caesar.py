from alphabet import letters
from alphabet import indexes as letters_indexes
import vigenere
encode_symbol = vigenere.encode_symbol

def encode(input, output, key):
    vigenere.encode(input, output, letters[int(key) % len(letters)])

def decode(input, output, key):
    vigenere.decode(input, output, letters[int(key) % len(letters)])
