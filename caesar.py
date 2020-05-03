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

def encode(input, output, key):
    while True:
        packet = input.read(packet_size)
        encoded_str = []
        for s in packet:
            encoded_str.append(encode_symbol(key, s))
        output.write("".join(encoded_str))
        if len(packet) < packet_size:
            break

def decode(input, output, key):
    encode(input, output, -key)
