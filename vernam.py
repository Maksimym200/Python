from vernam_alphabet import letters
from vernam_alphabet import indexes as letters_indexes
from math import log2, floor
encodable_size = 2 ** floor(log2(len(letters)))


def encode_symbol(key_s, s):
    
    if (not key_s in letters_indexes) or (not s in letters_indexes)\
       or letters_indexes[s] >= encodable_size or letters_indexes[key_s] >= encodable_size:
        return s
    else:
        return letters[letters_indexes[s] ^ letters_indexes[key_s]]

def encode(input, output, key):
    while True:
        packet = input.read(packet_size)
        encoded_str = []
        index = 0
        for s in packet:
            encoded_str.append(encode_symbol(key[index], s))
            index = (index + 1) % len(key)
        output.write("".join(encoded_str))
        if len(packet) < packet_size:
            break

def decode(input, output, key):
    encode(input, output, key)
