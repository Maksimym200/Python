import lib
import string


Data = lib.Data()
aID = Data.add_alphabet(string.ascii_letters, 'test alphabet')
mID = Data.add_model('model', 'test model', aID)

def test_objects():

    assert Data.get_alphabet_description(aID) == 'test alphabet'
    aID2 = Data.add_alphabet(string.ascii_lowercase, 'test alphabet 2')

    assert Data.get_alphabet_description(aID) == 'test alphabet'
    assert Data.get_alphabet_description(aID2) == 'test alphabet 2'

    assert Data.get_model_description(mID)[0] == aID

test_objects()

def test_encode():

    a = Data.encode('abracadabra', 'test', aID)
    assert Data.decode(a, 'test', aID) == 'abracadabra'

    b = Data.encode('abracadabra', 'testtesttesttest', aID)
    assert Data.decode(b, 'test', aID) == 'abracadabra'

    c = Data.encode('1$#80p', 'test', aID)
    assert Data.decode(c, 'test', aID) == '1$#80p'

test_encode()

def test_hack():

    Data.hack('abracadabra', mID)
    Data.hack('1$#80P', mID)

test_hack()

def test_crazy_inputs():

    assert Data.get_alphabet_description('-1') == None
    assert Data.get_alphabet('-1') == None
    assert Data.get_model_description('-1') == None
    assert Data.get_model('-1') == None

    Data.encode('abracadabra', '8888', aID)
    Data.encode('abracadabra', 'test', '-1')
    Data.decode('abracadabra', '8888', aID)
    Data.decode('abracadabra', 'test', '-1')
    Data.hack('abracadabra', '-1')
    
    Data.add_alphabet('aa', 'Two \'a\'')
    Data.add_model('aa', 'Two \'a\'', '-1')

test_crazy_inputs()
