import json
import vigenere
from contextlib import contextmanager
import hack as _hack
from strings import errors, objects


data_file = 'data.txt'


@contextmanager
def open_object(i, id):
    with open(f'{i}_{id}.txt', 'r') as obj:
        yield json.load(obj)


def write_object(i, id, data):
    with open(f'{i}_{id}.txt', 'w') as obj:
        json.dump(data, obj)


class Data:
    def __init__(self):
        with open(data_file, 'r') as data:
            info = json.load(data)
            self.models = info[1]
            self.alphabets = info[0]          

    def add_model(self, input, description, ID):
        alphabet = self.get_alphabet(ID)
        if not alphabet:
            return errors.no_alphabet()
        if not set(alphabet['letters']) & set(input):
            return errors.incorrect_model() + '\n' + errors.empty_model()
        index = str(len(self.models))
        self.models[index] = (ID, description)
        write_object(objects.model(), index, _hack.train(input, alphabet))
        with open(data_file, 'w') as data:
            json.dump((self.alphabets, self.models), data)
        return index

    def add_alphabet(self, alphabet_letters, description):
        if len(set(alphabet_letters)) < len(alphabet_letters):
            return errors.incorrect_alphabet() + '\n' + errors.duplicate_alphabet()
        if not alphabet_letters:
            return errors.incorrect_alphabet() + '\n' + errors.empty_alphabet()
        index = str(len(self.alphabets))
        self.alphabets[index] = description
        alphabet = {'letters' : alphabet_letters, \
                    'indexes' : {alphabet_letters[i] : i for i in range(len(alphabet_letters))}}
        write_object(objects.alphabet(), index, alphabet)
        with open(data_file, 'w') as data:
            json.dump((self.alphabets, self.models), data)
        return index

    def get_object_description(self, ID, obj):
        objects = self.__getattribute__(f'{obj}s')
        if ID not in objects:
            return None
        return objects[ID]

    def get_model_description(self, ID):
        return self.get_object_description(ID, objects.model())

    def get_alphabet_description(self, ID):
        return self.get_object_description(ID, objects.alphabet())

    def get_object(self, ID, obj):
        objects = self.__getattribute__(f'{obj}s')
        if ID not in objects:
            return None
        with open_object(obj, ID) as obj:
            return obj

    def get_model(self, ID):
        return self.get_object(ID, objects.model())

    def get_alphabet(self, ID):
        return self.get_object(ID, objects.alphabet())

    def encode(self, input, key, ID, shift = objects.encode()):
        alphabet = self.get_alphabet(ID)
        if not alphabet:
            return errors.no_alphabet()
        if not set(key) <= set(alphabet['letters']):
            return errors.incorrect_key()
        f = getattr(vigenere, shift)
        return f(input, key, alphabet)

    def decode(self, input, key, ID):
        return self.encode(input, key, ID, objects.decode())

    def hack(self, input, ID):
        model = self.get_model(ID)
        if not model:
            return errors.no_model()
        alphabet = self.get_alphabet(self.get_model_description(ID)[0])
        return _hack.hack(input, model, alphabet)
