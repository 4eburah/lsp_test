import json

def get_config():
    '''Returns user config'''
    with open('./config/config.json') as input_file:
        config = json.loads(input_file.read())

    return config

