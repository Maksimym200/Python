def encode_symbol(key, s, alphabet):
    letters = alphabet['letters']
    letters_indexes = alphabet['indexes']
    if s in letters_indexes:
        return letters[(letters_indexes[s] + int(key)) % len(letters)]
    else:
        return s

    
def encode_with_shift(text, key, a, shift = 1):
    encoded_str = []
    index = 0
    for s in text:
        encoded_str.append(encode_symbol(shift * a['indexes'][key[index]], s, a))
        index = (index + 1) % len(key)
    return "".join(encoded_str)


def encode(text, key, alphabet):
    return encode_with_shift(text, key, alphabet)


def decode(text, key, alphabet):
    return encode_with_shift(text, key, alphabet, -1)
