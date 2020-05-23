class methods:
    encode = '/encode'
    decode = '/decode'
    hack = '/hack'

    def action(_action):
        if _action in {'encode', 'decode', 'hack'}:
            return f'/{_action}'

    def add(obj):
        return '/add_' + obj

    def getinfo(obj):
        return '/getinfo_' + obj


class errors:
    error = '#Error '
    incorrect_ID = error + 'Incorrect ID'
    incorrect_key = error + 'Incorrect key'

    def unknown_object(_obj):
        return errors.error + f'Unknown object \'{_obj}\''

    no_file_input = error + 'Input file not found'
    no_file_output = error + 'Output file not found'
    no_alphabet = error + 'Alphabet not found'
    no_model = error + 'Model not found'
    incorrect_alphabet = error + 'Incorrect alphabet'
    incorrect_model = error + 'Incorrect model'

    def unknown_command(_command):
        return errors.error + f'Unknown command \'{_command}\''

    no_server = error + 'Server not found'

    empty_model = 'Model should contain symbols in alphabet'
    empty_alphabet = 'Alphabet should contain symbols'
    duplicate_alphabet = 'Alphabet should not contain same symbols'


class messages:
    _in = '- Input'
    _out = '- Output'

    def address(main_args, command):
        return f'http://{main_args.host}:{main_args.port}{command}'

    suggest_help = 'Type \'help\' to get help'
    help = 'Available commands:\n\
        - info {alphabet / model} : get alphabet or model information\n\
        - add {alphabet / model} : add alphabet or model\n\
        - encode : encode text with vigenere cipher\n\
        - decode : decode input with vigenere cipher\n\
        - hack : hack encoded text\n\
        - exit : exit the program'
    leave = 'Are you sure you want to leave (y/n)?  '
    enter_command = 'Enter command:  '

    def print_message(obj_1, obj_2):
        return f'Print {obj_1}{" " + obj_2 if not obj_2 is None else ""}:  '

    def print_input_file(action):
        return f'Print name of the file to {action} (Tap Enter to read from console):  '

    print_output_file = 'Print name of the file to save the result (Tap Enter to write to console):  '

    def print_object_file(obj):
        return f'Print {obj} file name (Tap Enter to read from console):  '
  
    no_info = 'No information found'

    def model_info(ID, info):
        return f'Model alphabet ID: {ID}\n{info}'

    def added(ID):
        return f'Added with ID: {ID}'


class objects:
    model = 'model'
    alphabet = 'alphabet'
    ID = 'ID'
    key = 'key'
    description = 'description'
    encode = 'encode'
    hack = 'hack'
    decode = 'decode'
    encrypt_commands = {encode, decode, hack}
    server_objects = {model, alphabet}
    
