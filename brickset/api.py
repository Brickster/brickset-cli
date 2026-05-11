from typing import Any

import requests
import sys

from . import config

_API = 'https://brickset.com/api/v3.asmx'


def execute_api_request(api: str, include_hash: bool = False, **kwargs: Any) -> dict[str, Any]:
    brickset_config = config.get_config()
    params = {'apiKey': brickset_config['api_key']}
    if include_hash:
        if 'hash' not in brickset_config:
            sys.exit('ERROR: user hash required. Run: brickset login')
        params['userHash'] = brickset_config['hash']
    for key, value in iter(kwargs.items()):
        params[key] = str(value)  # important when value='params' but str everything anyway

    response = requests.get(_API + '/' + api, params=params)
    if response.status_code != 200:
        print(response.text)
        sys.exit(f'ERROR: {api} API returned an unexpected error')
    response_json = response.json()
    if response_json['status'] != 'success':
        print(response.text)
        sys.exit(f'ERROR: {api} API returned an unexpected error')

    return response_json
