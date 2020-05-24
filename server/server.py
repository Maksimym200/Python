import flask
import lib
import json
import argparse
from constants import methods, objects, messages


app = flask.Flask('encryptor')
Data = lib.Data()


@app.route(methods.encode, methods=['GET'])
def encode():
    args = flask.request.args
    return Data.encode(str(args['input']), str(args['key']), str(args['ID']))


@app.route(methods.decode, methods=['GET'])
def decode():
    args = flask.request.args
    return Data.decode(str(args['input']), str(args['key']), str(args['ID']))


@app.route(methods.hack, methods=['GET'])
def hack():
    args = flask.request.args
    return Data.hack(str(args['input']), str(args['ID']))


@app.route(methods.add(objects.alphabet), methods=['POST'])
def add_alphabet():
    args = flask.request.args
    return str(Data.add_alphabet(str(args['input']), str(args['description'])))


@app.route(methods.add(objects.model), methods=['POST'])
def add_model():
    args = flask.request.args
    return str(Data.add_model(str(args['input']), str(args['description']), str(args['ID'])))


@app.route(methods.getinfo(objects.alphabet), methods=['GET'])
def getinfo_alphabet():
    ID = str(flask.request.args['ID'])
    alphabet_desc = Data.get_alphabet_description(ID)
    if not alphabet_desc:
        return messages.no_info
    return alphabet_desc


@app.route(methods.getinfo(objects.model), methods=['GET'])
def getinfo_model():
    ID = str(flask.request.args['ID'])
    model_desc = Data.get_model_description(ID)
    if model_desc is None:
        return messages.no_info
    return messages.model_info(model_desc[0], model_desc[1])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host')
    parser.add_argument('--port', type=int)
    args = parser.parse_args()
    app.run(args.host, args.port)
