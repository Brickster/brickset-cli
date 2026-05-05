import json
import os

from . import api
from .config import _config_directory

_CACHE_FILENAME = 'cache'


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
        set_number = lego_set['number'] + '-' + str(lego_set['numberVariant'])
        cache['sets'][lego_set['setID']] = set_number
        cache['sets'][set_number] = str(lego_set['setID'])
    save_cache(cache)
    return cache


def _get_set_number(set_id):
    cache = get_cache()
    if set_id not in cache['sets']:
        sets_json = api.execute_api_request('getSets', include_hash=True, params={'setID': set_id})
        cache = update_cache(sets_json['sets'])
    return cache['sets'].get(set_id, None)


def _get_id(set_number):
    cache = get_cache()
    if set_number not in cache['sets']:
        sets_json = api.execute_api_request('getSets', include_hash=True, params={'setNumber': set_number})
        cache = update_cache(sets_json['sets'], cache)
    return cache['sets'].get(set_number, None)


def id_to_set_number_generator(ids):
    for i in ids:
        yield _get_set_number(i)


def set_number_to_id_generator(set_numbers):
    for n in set_numbers:
        yield _get_id(n)
