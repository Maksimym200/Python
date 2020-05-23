import lib
import string
import pytest


def test_objects():
    Data = lib.Data()
    aID = Data.add_alphabet(string.ascii_letters, 'test alphabet')
    mID = Data.add_model('model', 'test model', aID)

    assert Data.get_alphabet_description(aID) == 'test alphabet'
    aID2 = Data.add_alphabet(string.ascii_lowercase, 'test alphabet 2')

    assert Data.get_alphabet_description(aID) == 'test alphabet'
    assert Data.get_alphabet_description(aID2) == 'test alphabet 2'

    assert Data.get_model_description(mID)[0] == aID


def test_encode():
    Data = lib.Data()
    aID = Data.add_alphabet(string.ascii_letters, 'test alphabet')

    a = Data.encode('abracadabra', 'test', aID)
    assert Data.decode(a, 'test', aID) == 'abracadabra'

    b = Data.encode('abracadabra', 'testtesttesttest', aID)
    assert Data.decode(b, 'test', aID) == 'abracadabra'

    c = Data.encode('1$#80p', 'test', aID)
    assert Data.decode(c, 'test', aID) == '1$#80p'


def test_hack():
    Data = lib.Data()
    aID = Data.add_alphabet(string.ascii_letters, 'test alphabet')
    mID = Data.add_model('model', 'test model', aID)

    Data.hack('abracadabra', mID)
    Data.hack('1$#80P', mID)


def test_crazy_inputs():
    Data = lib.Data()
    aID = Data.add_alphabet(string.ascii_letters, 'test alphabet')

    assert Data.get_alphabet_description('-1') is None
    assert Data.get_alphabet('-1') is None
    assert Data.get_model_description('-1') is None
    assert Data.get_model('-1') is None

    Data.encode('abracadabra', '8888', aID)
    Data.encode('abracadabra', 'test', '-1')
    Data.decode('abracadabra', '8888', aID)
    Data.decode('abracadabra', 'test', '-1')
    Data.hack('abracadabra', '-1')
    
    Data.add_alphabet('aa', 'Two \'a\'')
    Data.add_model('aa', 'Two \'a\'', '-1')
    Data.add_alphabet('', 'Null')
    Data.add_model('12345', '12345', aID)
