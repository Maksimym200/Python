letters = []
letters_indexes = dir()

def import_alphabet(_letters, _letters_indexes):
    global letters
    global letters_indexes
    letters = _letters
    letters_indexes = _letters_indexes  

def encode_symbol(key, s):
    if s in letters_indexes:
        return letters[(letters_indexes[s] + key) % len(letters)]
    elif s.lower() in letters_indexes:
        return letters[(letters_indexes[s.lower()] + key) % len(letters)].upper()
    else:
        return s

def encode(input, output, key):
    while not input.closed:
        part = input.read(1024)
        encoded_str = []
        for s in part:
            encoded_str.append(encode_symbol(key, s))
        output.write("".join(encoded_str))
        if len(part) < 1024:
            break

def decode(input, output, key):
    encode(input, output, -key)
