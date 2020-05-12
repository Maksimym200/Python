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
        if alphabet == None:
            return ' Error# Alphabet not found'
        if len(set(alphabet['letters']) & set(input)) == 0:
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
        if len(alphabet_letters) == 0:
            return ' Error# Incorrect alphabet. Alphabet should contain symbols'
        index = str(len(self.alphabets))
        self.alphabets[index] = description
        alphabet = {'letters' : alphabet_letters, \
                    'indexes' : {alphabet_letters[i] : i for i in range(len(alphabet_letters))}}
        write_object('alphabet', index, alphabet)
        with open('data.txt', 'w') as data:
            json.dump((self.alphabets, self.models), data)
        return index

    def get_model_description(self, ID):
        if not ID in self.models:
            return None
        return self.models[ID]

    def get_alphabet_description(self, ID):
        if not ID in self.alphabets:
            return None
        return self.alphabets[ID]

    def get_model(self, ID):
        if not ID in self.models:
            return None
        with open_object('model', ID) as model:
            return model

    def get_alphabet(self, ID):
        if not ID in self.alphabets:
            return None
        with open_object('alphabet', ID) as alphabet:
            return alphabet

    def encode(self, input, key, ID):
        alphabet = self.get_alphabet(ID)
        if alphabet == None:
            return ' #Error Alphabet not found'
        if not set(key) <= set(alphabet['letters']):
            return ' #Error Alphabet don\'t support some of Key symbols'
        return vigenere.encode(input, key, alphabet)

    def decode(self, input, key, ID):
        alphabet = self.get_alphabet(ID)
        if alphabet == None:
            return ' #Error Alphabet not found'
        if not set(key) <= set(alphabet['letters']):
            return ' #Error Alphabet don\'t support some of Key symbols'
        return vigenere.decode(input, key, alphabet)

    def hack(self, input, ID):
        model = self.get_model(ID)
        if model == None:
            return ' #Error Model not found'
        alphabet = self.get_alphabet(self.get_model_description(ID)[0])
        return _hack.hack(input, model, alphabet)
