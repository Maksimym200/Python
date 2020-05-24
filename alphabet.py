from string import ascii_letters as english
from string import digits as digits
from string import punctuation as punctuation
russian = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
letters = english + russian + digits + punctuation + ' \n'
indexes = {letters[i] : i for i in range(len(letters))}
