letters = []
letters_indexes = dir()

def import_alphabet(_letters, _letters_indexes):
    global letters
    global letters_indexes
    letters = _letters
    letters_indexes = _letters_indexes  

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
    encode(input, output, key)
