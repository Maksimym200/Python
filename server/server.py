import flask
import lib
import json


app = flask.Flask('encryptor')
Data = lib.Data()


@app.route('/encode', methods=['GET'])
def encode():
    args = flask.request.args
    return Data.encode(str(args['input']), str(args['key']), str(args['ID']))


@app.route('/decode', methods=['GET'])
def decode():
    args = flask.request.args
    return Data.decode(str(args['input']), str(args['key']), str(args['ID']))


@app.route('/hack', methods=['GET'])
def hack():
    args = flask.request.args
    return Data.hack(str(args['input']), str(args['ID']))


@app.route('/add_alphabet', methods=['POST'])
def add_alphabet():
    args = flask.request.args
    return str(Data.add_alphabet(str(args['input']), str(args['description'])))


@app.route('/add_model', methods=['POST'])
def add_model():
    args = flask.request.args
    return str(Data.add_model(str(args['input']), str(args['description']), str(args['ID'])))


@app.route('/get_alphabet_information', methods=['GET'])
def get_alphabet_information():
    ID = str(flask.request.args['ID'])
    alphabet_desc = Data.get_alphabet_description(ID)
    if alphabet_desc is None:
        return ' No information found'
    return alphabet_desc


@app.route('/get_model_information', methods=['GET'])
def get_model_information():
    ID = str(flask.request.args['ID'])
    model_desc = Data.get_model_description(ID)
    if model_desc is None:
        return ' No information found'
    return f'Model alphabet ID: {model_desc[0]}\n {model_desc[1]}'


if __name__ == '__main__':
    app.run('::', port=8888)
