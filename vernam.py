from vernam_alphabet import letters
from vernam_alphabet import indexes as letters_indexes


def encode_symbol(key_s, s):
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
