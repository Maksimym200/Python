from sys import stdout as _out
from sys import stdin as _in
import json as _json
from collections import Counter as _Counter

def _encode_symbol(_key, _s):
    if not _s.isalpha():
        return _s
    elif _s.islower():
        return chr((ord(_s) - ord('a') + _key) % 26 + ord('a'))
    else:
        return chr((ord(_s) - ord('A') + _key) % 26 + ord('A'))

def stream_encode(_key, _input, _output):
    while True:
        try:
            _s = _input.read(1)
        except:
            break
        if _s == "":
            break
        _output.write(_encode_symbol(_key, _s))

def stream_decode(_key, _input, _output):
    while True:
        try:
            _s = _input.read(1)
        except:
            break
        if _s == "":
            break
        _output.write(_encode_symbol(-_key, _s))

def encode(_key, _input_name, _output_name):
    _input = _in
    _output = _out
    if _input_name != None:
        _input = open(_input_name, 'r')
    if _output_name != None:
        _output = open(_output_name, 'w')
    stream_encode(int(_key), _input, _output)
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
    stream_decode(int(_key), _input, _output)
    if _input_name != None:
        _input.close()
    if _output_name != None:
        _output.close()

def _get_frequency_data(_data):
    _frequency_data = dict()
    _data_size = sum(_data.values())
    for _s in _data:
        _frequency_data[_s] = (_data[_s] / _data_size)
    for i in range(128):
        if not(chr(i) in _frequency_data):
            _frequency_data[chr(i)] = 0
    return _frequency_data

def _get_key(_frequency_data, _model):
    _key = 0
    _similarity = 1
    for _i in range(26):
        _current_simularity = 0
        for _s in _model:
            if _encode_symbol(_i, _s) not in _frequency_data:
                _current_simularity += _model[_s]
            else:
               _current_simularity += abs(_frequency_data[_encode_symbol(_i, _s)] - _model[_s])
        if (_current_simularity <= _similarity):
            _similarity = _current_simularity
            _key = _i
    return _key

def stream_train(_input, _model):
    _data = _Counter()
    while True:
        try:
            _s = _input.read(1)
        except:
            break
        if _s == "":
            break
        _data += _Counter({_s})
    _json.dump(_get_frequency_data(_data), _model)

def stream_hack(_input, _output, _model):
    _text = []
    _text_data = _Counter()
    while True:
        try:
            _s = _input.read(1)
        except:
            break
        if _s == "":
            break
        _text_data += _Counter({_s})
        _text.append(_s)
    _text_frequency_data = _get_frequency_data(_text_data)
    _key = _get_key(_text_frequency_data, _model)
    for i in range(len(_text)):
        _output.write(_encode_symbol(-_key, _text[i]))

def train(_input_name, _model_name):
    _input = _in
    if _input_name != None:
        _input = open(_input_name, 'r')
    _model = open(_model_name, 'w')
    stream_train(_input, _model)
    if _input_name != None:
        _input.close()

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
