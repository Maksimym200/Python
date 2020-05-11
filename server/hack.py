import json
from vigenere import encode_symbol
from collections import defaultdict
accuracy = 0.005

def get_data_list(text, key_len, alphabet):
        data_list = []
        for i in range(key_len):
            data_list.append(defaultdict(int))
        for i in range(len(text)):
            if text[i] in alphabet['letters']:
                data_list[i % key_len][text[i]] += 1
        return data_list

def get_frequency_data(data, alphabet):
    frequency_data = defaultdict(int)
    data_size = sum(data.values())
    for s in data:
        frequency_data[s] = (data[s] / data_size)
    for i in alphabet['letters']:
        if i not in frequency_data:
            frequency_data[i] = 0
    return frequency_data

def index_of_coincidence(frequency_data):
    index = 0
    for s in frequency_data:
        index += (frequency_data[s] ** 2)
    return index

def get_correct_frequency_data_list(text, index, alphabet):
    correct_frequency_data_list = []
    current_index = 0
    max_len = len(text) / 2
    key_len = 0
    while (key_len <= max_len):
        key_len += 1
        data_list = get_data_list(text, key_len, alphabet)
        frequency_data_list = []
        average_index = 0
        for data in data_list:
            frequency_data_list.append(get_frequency_data(data, alphabet))
            average_index += index_of_coincidence(frequency_data_list[-1])
        average_index /= key_len
        if (average_index > current_index):
            correct_frequency_data_list = frequency_data_list
            current_index = average_index
        if abs(average_index - index) < accuracy and max_len == len(text) / 2:
            max_len = key_len * 2
    return correct_frequency_data_list

        
def get_key(text, model, alphabet):
    index = index_of_coincidence(get_frequency_data(model, alphabet))
    frequency_data_list = get_correct_frequency_data_list(text, index, alphabet)
    key_len = len(frequency_data_list)
    key = []
    for frequency_data in frequency_data_list:
        key_symbol = 0
        similarity = 1
        for i in range(len(alphabet['letters'])):
            current_similarity = 0
            for s in model:
                current_similarity += abs(frequency_data[encode_symbol(i, s, alphabet)] - model[s])
            if (current_similarity <= similarity):
                similarity = current_similarity
                key_symbol = i
        key.append(key_symbol)
    return key


def hack(text, model, alphabet):
    key = get_key(text, model, alphabet)
    index = 0
    decoded_text = []
    for s in text:
        decoded_text.append(encode_symbol(-key[index], s, alphabet))
        index = (index + 1) % len(key)
    return "".join(decoded_text)


def train(text, alphabet):
    data = defaultdict(int)
    for s in text:
        if s in alphabet['indexes']:
            data[s] += 1
    return get_frequency_data(data, alphabet)

