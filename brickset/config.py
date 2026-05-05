import json
import os
import sys

_BRICKSET_DIRECTORY = '.brickset'
_CONFIG_FILENAME = 'config'


def _config_directory():
    return os.path.expanduser('~') + os.sep + _BRICKSET_DIRECTORY + os.sep


def get_config():
    config_path = _config_directory() + _CONFIG_FILENAME
    if not os.path.exists(config_path):
        sys.exit('ERROR: no config exists. Run: brickset config API_KEY')
    with open(config_path, 'r') as config_file:
        return json.load(config_file)


def configure(api_key):
    config_dir = _config_directory()
    if not os.path.exists(config_dir):
        os.mkdir(config_dir)
    with open(config_dir + _CONFIG_FILENAME, 'w') as config_file:
        json.dump({'api_key': api_key}, config_file)
