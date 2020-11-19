import getpass
import json
import os
import sys
from datetime import datetime

import pytz

import api

_BRICKSET_DIRECTORY = '.brickset'
_CONFIG_FILENAME = 'config'
_CACHE_FILENAME = 'cache'


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


def show_usage(mode):
    usage_json = api.execute_api_request('getKeyUsageStats')
    if mode == 'ALL':
        for usage_day in usage_json['apiKeyUsage']:
            print '{}: {}'.format(usage_day['dateStamp'], usage_day['count'])
    else:
        if len(usage_json['apiKeyUsage']) > 0:
            last_usage_date = usage_json['apiKeyUsage'][0]['dateStamp']
            # the usage limits actually rollover in BST, not UTC
            today = datetime.now(tz=pytz.timezone('Europe/London')).strftime('%Y-%m-%dT00:00:00Z')
            if mode == 'LAST' or last_usage_date == today:
                print '{}: {}'.format(last_usage_date, usage_json['apiKeyUsage'][0]['count'])
            else:
                print '{}: {}'.format(today, 0)


def log_in():
    username = raw_input('Username: ')
    password = getpass.getpass('Password (only used to retrieve user hash): ')

    brickset_config = get_config()
    user_hash_json = api.execute_api_request('login', username=username, password=password)

    brickset_config['hash'] = user_hash_json['hash']
    with open(_config_directory() + _CONFIG_FILENAME, 'w') as config_file:
        json.dump(brickset_config, config_file)


def get_cache():
    cache_file = _config_directory() + _CACHE_FILENAME
    if not os.path.exists(cache_file):
        return {'sets': {}}
    with open(cache_file, 'r') as f:
        return json.load(f)


def save_cache(cache):
    with open(_config_directory() + _CACHE_FILENAME, 'w') as f:
        json.dump(cache, f, indent=2)


def update_cache(sets, cache=None):
    cache = get_cache() if cache is None else cache
    for lego_set in sets:
        # store ID <-> number
        set_number = lego_set['number'] + '-' + str(lego_set['numberVariant'])
        cache['sets'][lego_set['setID']] = set_number
        cache['sets'][set_number] = str(lego_set['setID'])
    save_cache(cache)
    return cache
