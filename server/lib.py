import json
import vigenere
from contextlib import contextmanager
import hack as _hack


@contextmanager
def open_object(i, id):
    with open(f'{i}_{id}.txt', 'r') as object:
        yield json.load(object)


def write_object(i, id, data):
    with open(f'{i}_{id}.txt', 'w') as object:
        json.dump(data, object)


class Data:
    def __init__(self):
        with open('data.txt', 'r') as data:
            info = json.load(data)
            self.models = info[1]
            self.alphabets = info[0]          

    def add_model(self, input, description, ID):
        alphabet = self.get_alphabet(ID)
        if not alphabet:
            return ' Error# Alphabet not found'
        if not set(alphabet['letters']) & set(input):
            return ' Error# Incorrect model. Model should contain symbols in alphabet'
        index = str(len(self.models))
        self.models[index] = (ID, description)
        write_object('model', index, _hack.train(input, alphabet))
        with open('data.txt', 'w') as data:
            json.dump((self.alphabets, self.models), data)
        return index

    def add_alphabet(self, alphabet_letters, description):
        if len(set(alphabet_letters)) < len(alphabet_letters):
            return  ' Error# Incorrect alphabet. Alphabet should not contain same symbols'
        if not alphabet_letters:
            return ' Error# Incorrect alphabet. Alphabet should contain symbols'
        index = str(len(self.alphabets))
        self.alphabets[index] = description
        alphabet = {'letters' : alphabet_letters, \
                    'indexes' : {alphabet_letters[i] : i for i in range(len(alphabet_letters))}}
        write_object('alphabet', index, alphabet)
        with open('data.txt', 'w') as data:
            json.dump((self.alphabets, self.models), data)
        return index

    def get_object_description(self, ID, object):
        objects = self.__getattribute__(f'{object}s')
        if ID not in objects:
            return None
        return objects[ID]

    def get_model_description(self, ID):
        return self.get_object_description(ID, 'model')

    def get_alphabet_description(self, ID):
        return self.get_object_description(ID, 'alphabet')

    def get_object(self, ID, object):
        objects = self.__getattribute__(f'{object}s')
        if ID not in objects:
            return None
        with open_object(object, ID) as obj:
            return obj

    def get_model(self, ID):
        return self.get_object(ID, 'model')

    def get_alphabet(self, ID):
        return self.get_object(ID, 'alphabet')

    def encode(self, input, key, ID, shift = 'encode'):
        alphabet = self.get_alphabet(ID)
        if not alphabet:
            return ' #Error Alphabet not found'
        if not set(key) <= set(alphabet['letters']):
            return ' #Error Alphabet don\'t support some of Key symbols'
        f = getattr(vigenere, shift)
        return f(input, key, alphabet)

    def decode(self, input, key, ID):
        return self.encode(input, key, ID, 'decode')

    def hack(self, input, ID):
        model = self.get_model(ID)
        if not model:
            return ' #Error Model not found'
        alphabet = self.get_alphabet(self.get_model_description(ID)[0])
        return _hack.hack(input, model, alphabet)
