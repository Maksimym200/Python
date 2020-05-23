class methods:
    def encode():
        return '/encode'

    def decode():
        return '/decode'

    def hack():
        return '/hack'

    def action(_action):
        if _action in {'encode', 'decode', 'hack'}:
            return f'/{_action}'

    def add(obj):
        return '/add_' + obj

    def getinfo(obj):
        return '/getinfo_' + obj

    def name():
        return '/encryptor'


class errors:
    def error():
        return '#Error '

    def incorrect_ID():
        return errors.error() + 'Incorrect ID'

    def incorrect_key():
        return errors.error() + 'Incorrect key'

    def unknown_object(_obj):
        return errors.error() + f'Unknown object \'{_obj}\''

    def no_file_input():
        return errors.error() + 'Input file not found'

    def no_file_output():
        return errors.error() + 'Output file not found'

    def no_alphabet():
        return errors.error() + 'Alphabet not found'

    def no_model():
        return errors.error() + 'Model not found'

    def incorrect_alphabet():
        return errors.error() + 'Incorrect alphabet'

    def incorrect_model():
        return errors.error() + 'Incorrect model'

    def unknown_command(_command):
        return errors.error() + f'Unknown command \'{_command}\''

    def no_server():
        return errors.error() + 'Server not found'

    def empty_model():
        return 'Model should contain symbols in alphabet'

    def empty_alphabet():
        return 'Alphabet should contain symbols'

    def duplicate_alphabet():
        return 'Alphabet should not contain same symbols'


class messages:
    def _in():
        return '- Input'

    def _out():
        return '- Output'

    def address(main_args, command):
        return f'http://{main_args.host}:{main_args.port}{command}'

    def suggest_help():
        return 'Type \'help\' to get help'

    def help():
        return 'Available commands:\n\
        - info {alphabet / model} : get alphabet or model information\n\
        - add {alphabet / model} : add alphabet or model\n\
        - encode : encode text with vigenere cipher\n\
        - decode : decode input with vigenere cipher\n\
        - hack : hack encoded text\n\
        - exit : exit the program'

    def leave():
        return 'Are you sure you want to leave (y/n)?  '

    def enter_command():
        return 'Enter command:  '

    def print_message(obj_1, obj_2):
        return f'Print {obj_1}{" " + obj_2 if not obj_2 is None else ""}:  '

    def print_input_file(action):
        return f'Print name of the file to {action} (Tap Enter to read from console):  '

    def print_output_file():
        return f'Print name of the file to save the result (Tap Enter to write to console):  '

    def print_object_file(obj):
        return f'Print {obj} file name (Tap Enter to read from console):  '
  
    def no_info():
        return 'No information found'

    def model_info(ID, info):
        return f'Model alphabet ID: {ID}\n{info}'

    def added(ID):
        return f'Added with ID: {ID}'


class objects:
    def model():
        return 'model'

    def alphabet():
        return 'alphabet'

    def ID():
        return 'ID'

    def key():
        return 'key'

    def description():
        return 'description'

    def encode():
        return 'encode'

    def hack():
        return 'hack'

    def decode():
        return 'decode'

    def encrypt_commands():
        return {objects.encode(), objects.decode(), objects.hack()}

    def server_objects():
        return {objects.model(), objects.alphabet()}
        
