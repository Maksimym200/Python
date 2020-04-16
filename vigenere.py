from sys import stdout
from sys import stdin
import json
from collections import Counter
from string import ascii_lowercase as letters
letters_indexes = {letters[i] : i for i in range(len(letters))}

def get_name_supporing_function(f):
    def name_supporing_function(*args):
        if args[0] == None:
            if args[1] == None:
                f(stdin, stdout, *args[2:])
            else:
                with open(args[1], 'w') as output:
                    f(stdin, output, *args[2:])
        else:
            if args[1] == None:
                with open(args[0], 'r') as input:
                    f(input, stdout, *args[2:])
            else:
                with open(args[0], 'r') as input:
                    with open(args[1], 'w') as output:
                        f(input, output, *args[2:])
    return name_supporing_function

def encode_symbol(key, s):
    if not s.isalpha():
        return s
    elif s.islower():
        return letters[(letters_indexes[s] + key) % len(letters)]
    else:
        return letters[(letters_indexes[s.lower()] + key) % len(letters)].upper()

def stream_encode(input, output, key):
    index = 0
    while True:
        try:
            s = input.read(1)
        except:
            break
        if s == "":
            break
        output.write(encode_symbol(letters_indexes[key[index].lower()], s))
        index = (index + 1) % len(key)

def stream_decode(input, output, key):
    index = 0
    while True:
        try:
            s = input.read(1)
        except:
            break
        if s == "":
            break
        output.write(encode_symbol(-letters_indexes[key[index].lower()], s))
        index = (index + 1) % len(key)

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


def stream_hack(input, output, model_name):
    with open(model_name, "r") as model_encoded:
        model = json.load(model_encoded)
    text = []
    while True:
        try:
            s = input.read(1)
        except:
            break
        if s == "":
            break
        text.append(s)
    key = get_key(text, model)
    for i in range(len(text)):
        output.write(encode_symbol(-key[i % len(key)], text[i]))

def stream_train(input, model):
    data = Counter()
    while True:
        try:
            s = input.read(1)
        except:
            break
        if s == "":
            break
        if s.isalpha():
            data += Counter({s.lower()})
    json.dump(get_frequency_data(data), model)

decode = get_name_supporing_function(stream_decode)

encode = get_name_supporing_function(stream_encode)

hack = get_name_supporing_function(stream_hack)

train = get_name_supporing_function(stream_train)
