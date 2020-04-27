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
    while True:
        part = input.read(1024)
        if part == "":
            break
        encoded_str = []
        index = 0
        for s in part:
            encoded_str.append(encode_symbol(key[index], s))
            index = (index + 1) % len(key)
        output.write("".join(encoded_str))
        if len(part) < 1024:
            break

def decode(input, output, key):
    text = input.read()
    encoded_str = []
    index = 0
    for s in text:
        encoded_str.append(encode_symbol(-letters_indexes[key[index].lower()], s))
        index = (index + 1) % len(key)
        if len(encoded_str) == 1024:
            output.write("".join(encoded_str))
            encoded_str = []
    output.write("".join(encoded_str))
