import getpass
import json
from datetime import datetime

import pytz

from . import api
from .config import _config_directory, get_config

_CONFIG_FILENAME = 'config'


def show_usage(mode):
    usage_json = api.execute_api_request('getKeyUsageStats')
    if mode == 'ALL':
        for usage_day in usage_json['apiKeyUsage']:
            print('{}: {}'.format(usage_day['dateStamp'], usage_day['count']))
    else:
        if len(usage_json['apiKeyUsage']) > 0:
            last_usage_date = usage_json['apiKeyUsage'][0]['dateStamp']
            # the usage limits actually rollover in BST, not UTC
            today = datetime.now(tz=pytz.timezone('Europe/London')).strftime('%Y-%m-%dT00:00:00Z')
            if mode == 'LAST' or last_usage_date == today:
                print('{}: {}'.format(last_usage_date, usage_json['apiKeyUsage'][0]['count']))
            else:
                print('{}: {}'.format(today, 0))


def log_in():
    username = input('Username: ')
    password = getpass.getpass('Password (only used to retrieve user hash): ')

    brickset_config = get_config()
    user_hash_json = api.execute_api_request('login', username=username, password=password)

    brickset_config['hash'] = user_hash_json['hash']
    with open(_config_directory() + _CONFIG_FILENAME, 'w') as config_file:
        json.dump(brickset_config, config_file)