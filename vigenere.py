from sys import stdout as _out
from sys import stdin as _in

def _encode_symbol(_key_s, _s):
    if not _s.isalpha():
        return _s
    elif _s.islower():
        return chr((ord(_s) - ord('a') + ord(_key_s)) % 26 + ord('a'))
    else:
        return chr((ord(_s) - ord('A') + ord(_key_s)) % 26 + ord('A'))

def _decode_symbol(_key_s, _s):
    if not _s.isalpha():
        return _s
    elif _s.islower():
        return chr((ord(_s) - ord('a') - ord(_key_s)) % 26 + ord('a'))
    else:
        return chr((ord(_s) - ord('A') - ord(_key_s)) % 26 + ord('A'))

def stream_encode(_key, _input, _output):
    index = 0
    while True:
        try:
            _s = _input.read(1)
        except:
            break
        if _s == "":
            break
        _output.write(_encode_symbol(_key[index], _s))
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
        _output.write(_decode_symbol(_key[index], _s))
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
