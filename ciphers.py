import caesar
import vigenere
import vernam

def get_cipher(name):
    if name == 'caesar':
        return caesar
    elif name == 'vigenere':
        return vigenere
    elif name == 'vernam':
        return vernam
