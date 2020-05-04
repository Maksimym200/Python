from alphabet import letters
from alphabet import indexes as letters_indexes
packet_size = 1024

def encode_symbol(key, s):
    if s in letters_indexes:
        return letters[(letters_indexes[s] + int(key)) % len(letters)]
    elif s.lower() in letters_indexes:
        return letters[(letters_indexes[s.lower()] + int(key)) % len(letters)].upper()
    else:
        return s

def encode_with_shift(input, output, key, shift = 1):
    while True:
        packet = input.read(packet_size)
        encoded_str = []
        index = 0
        for s in packet:
            encoded_str.append(encode_symbol(shift * letters_indexes[key[index].lower()], s))
            index = (index + 1) % len(key)
        output.write("".join(encoded_str))
        if len(packet) < packet_size:
            break

def encode(input, output, key):
    encode_with_shift(input, output, key)

def decode(input, output, key):
    encode_with_shift(input, output, key, -1)
