import json
from collections import Counter

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

def get_data_list(text, key):
    data_list = []
    for i in range(key):
        data_list.append(Counter())
    for i in range(len(text)):
        if text[i].isalpha():
            data_list[i % key] += Counter({text[i].lower()})
    return data_list

def get_frequency_data(data):
    frequency_data = dict()
    data_size = sum(data.values())
    for s in data:
        frequency_data[s] = (data[s] / data_size)
    for i in letters:
        if not(i in frequency_data):
            frequency_data[i] = 0
    return frequency_data

def index_of_coincidence(frequency_data):
    index = 0
    for s in frequency_data:
        index += (frequency_data[s] ** 2)
    return index

def get_correct_frequency_data_list(text, index):
    correct_frequency_data_list = []
    current_index = 0
    for i in range(1, len(text) + 1, 1):
        data_list = get_data_list(text, i)
        frequency_data_list = []
        average_index = 0
        for j in range(i):
            frequency_data_list.append(get_frequency_data(data_list[j]))
            average_index += index_of_coincidence(frequency_data_list[j])
        average_index /= i
        if (average_index > current_index):
            correct_frequency_data_list = frequency_data_list
            current_index = average_index
        if abs(average_index - index) < 0.005:
            return frequency_data_list
    return correct_frequency_data_list

        
def get_key(text, model):
    index = index_of_coincidence(get_frequency_data(model))
    frequency_data_list = get_correct_frequency_data_list(text, index)
    key_len = len(frequency_data_list)
    key = []
    for j in range(key_len):
        key_symbol = 0
        similarity = 1
        for i in range(len(letters)):
            current_similarity = 0
            for s in model:
                current_similarity += abs(frequency_data_list[j][encode_symbol(i, s)] - model[s])
            if (current_similarity <= similarity):
                similarity = current_similarity
                key_symbol = i
        key.append(key_symbol)
    return key


def hack(input, output, model_name):
    with open(model_name, "r") as model_encoded:
        model = json.load(model_encoded)
    text = list(input.read())
    key = get_key(text, model)
    hacked_str = []
    for i in range(len(text)):
        hacked_str.append(encode_symbol(-key[i % len(key)], text[i]))
        if len(hacked_str) == 1024:
            output.write("".join(hacked_str))
            hacked_str.clear()
    output.write("".join(hacked_str))


def train(input, model):
    data = Counter()
    text = input.read()
    for s in text:
        if s.lower() in letters_indexes:
            data += Counter({s.lower()})
    json.dump(get_frequency_data(data), model)
