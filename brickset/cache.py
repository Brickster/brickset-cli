import json
from collections.abc import Iterator
from typing import Any

from . import api
from .config import _config_directory

_CACHE_FILENAME = 'cache'


def get_cache() -> dict[str, Any]:
    cache_file = _config_directory() / _CACHE_FILENAME
    if not cache_file.exists():
        return {'sets': {}}
    with open(cache_file, 'r') as f:
        return json.load(f)


def save_cache(cache: dict[str, Any]) -> None:
    with open(_config_directory() / _CACHE_FILENAME, 'w') as f:
        json.dump(cache, f, indent=2)


def update_cache(sets: list[dict[str, Any]], cache: dict[str, Any] | None = None) -> dict[str, Any]:
    cache = get_cache() if cache is None else cache
    for lego_set in sets:
        set_number = lego_set['number'] + '-' + str(lego_set['numberVariant'])
        cache['sets'][lego_set['setID']] = set_number
        cache['sets'][set_number] = str(lego_set['setID'])
    save_cache(cache)
    return cache


def _get_set_number(set_id: str) -> str | None:
    cache = get_cache()
    if set_id not in cache['sets']:
        sets_json = api.execute_api_request('getSets', include_hash=True, params={'setID': set_id})
        cache = update_cache(sets_json['sets'])
    return cache['sets'].get(set_id)


def _get_id(set_number: str) -> str | None:
    cache = get_cache()
    if set_number not in cache['sets']:
        sets_json = api.execute_api_request('getSets', include_hash=True, params={'setNumber': set_number})
        cache = update_cache(sets_json['sets'], cache)
    return cache['sets'].get(set_number)


def id_to_set_number_generator(ids: list[str]) -> Iterator[str | None]:
    yield from (_get_set_number(i) for i in ids)


def set_number_to_id_generator(set_numbers: list[str]) -> Iterator[str | None]:
    yield from (_get_id(n) for n in set_numbers)
