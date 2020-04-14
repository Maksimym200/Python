from sys import stdout as _out
from sys import stdin as _in
import json as _json
from collections import Counter as _Counter
from string import ascii_letters as _letters

def _encode_symbol(_key, _s):
    if not _s.isalpha():
        return _s
    elif _s.islower():
        return chr((ord(_s) - ord('a') + _key) % 26 + ord('a'))
    else:
        return chr((ord(_s) - ord('A') + _key) % 26 + ord('A'))

def stream_encode(_key, _input, _output):
    index = 0
    while True:
        try:
            _s = _input.read(1)
        except:
            break
        if _s == "":
            break
        _output.write(_encode_symbol(ord(_key[index]), _s))
        index = (index + 1) % len(_key)

def stream_decode(_key, _input, _output):
    index = 0
    while True:
        try:
            _s = _input.read(1)
        except:
            break
        if _s == "":
            break
        _output.write(_encode_symbol(-ord(_key[index]), _s))
        index = (index + 1) % len(_key)

def encode(_key, _input_name, _output_name):
    _input = _in
    _output = _out
    if _input_name != None:
        _input = open(_input_name, 'r')
    if _output_name != None:
        _output = open(_output_name, 'w')
    stream_encode(str(_key), _input, _output)
    if _input_name != None:
        _input.close()
    if _output_name != None:
        _output.close()

def decode(_key, _input_name, _output_name):
    _input = _in
    _output = _out
    if _input_name != None:
        _input = open(_input_name, 'r')
    if _output_name != None:
        _output = open(_output_name, 'w')
    stream_decode(str(_key), _input, _output)
    if _input_name != None:
        _input.close()
    if _output_name != None:
        _output.close()

def _get_data_list(_text, _key):
    _data_list = []
    for _i in range(_key):
        _data_list.append(_Counter())
    for _i in range(len(_text)):
        if _text[_i].isalpha():
            _data_list[_i % _key] += _Counter({_text[_i]})
    return _data_list

def _get_frequency_data(_data):
    _frequency_data = dict()
    _data_size = sum(_data.values())
    for _s in _data:
        _frequency_data[_s] = (_data[_s] / _data_size)
    for _i in _letters:
        if not(_i in _frequency_data):
            _frequency_data[_i] = 0
    return _frequency_data

def _index_of_coincidence(_frequency_data):
    _index = 0
    for _s in _frequency_data:
        _index += (_frequency_data[_s] ** 2)
    return _index

def _get_correct_frequency_data_list(_text, _index):
    _correct_frequency_data_list = []
    _current_index = 0
    for _i in range(1, len(_text) + 1, 1):
        _data_list = _get_data_list(_text, _i)
        _frequency_data_list = []
        _average_index = 0
        for _j in range(_i):
            _frequency_data_list.append(_get_frequency_data(_data_list[_j]))
            _average_index += _index_of_coincidence(_frequency_data_list[_j])
        _average_index /= _i
        if (_average_index > _current_index):
            _correct_frequency_data_list = _frequency_data_list
            _current_index = _average_index
        if abs(_average_index - _index) < 0.005:
            return _frequency_data_list
    return _correct_frequency_data_list

        
def _get_key(_text, _model):
    _index = _index_of_coincidence(_get_frequency_data(_model))
    _frequency_data_list = _get_correct_frequency_data_list(_text, _index)
    _key_len = len(_frequency_data_list)
    print(_key_len)
    _key = []
    for _j in range(_key_len):
        _key_symbol = 0
        _similarity = 1
        for _i in range(26):
            _current_similarity = 0
            for _s in _model:
                if _encode_symbol(_i, _s) not in _frequency_data_list[_j]:
                    _current_similarity += _model[_s]
                else:
                    _current_similarity += abs(_frequency_data_list[_j][_encode_symbol(_i, _s)] - _model[_s])
            if (_current_similarity <= _similarity):
                _similarity = _current_similarity
                _key_symbol = _i
        _key.append(_key_symbol)
    return _key


def stream_hack(_input, _output, _model):
    _text = []
    while True:
        try:
            _s = _input.read(1)
        except:
            break
        if _s == "":
            break
        _text.append(_s)
    _key = _get_key(_text, _model)
    for i in range(len(_text)):
        _output.write(_encode_symbol(-_key[i % len(_key)], _text[i]))

def hack(_input_name, _output_name, _model_name):
    _input = _in
    _output = _out
    if _input_name != None:
        _input = open(_input_name, 'r')
    if _output_name != None:
        _output = open(_output_name, 'w')
    with open(_model_name, "r") as _model_encoded:
        _model = _json.load(_model_encoded)
    stream_hack(_input, _output, _model)
    if _input_name != None:
        _input.close()
    if _output_name != None:
        _output.close()
