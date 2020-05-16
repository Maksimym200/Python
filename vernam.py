from alphabet import letters
from alphabet import indexes as letters_indexes
packet_size = 1024

def encode_symbol(key_s, s):
    if (not key_s.lower() in letters_indexes) or (not s.lower() in letters_indexes)\
       or letters_indexes[s.lower()] ^ letters_indexes[key_s.lower()] >= len(letters):
        return s
    elif s in letters_indexes:
        return letters[letters_indexes[s] ^ letters_indexes[key_s.lower()]]
    else:
        return letters[letters_indexes[s.lower()] ^ letters_indexes[key_s.lower()]].upper()

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
