from __future__ import print_function

from . import api


def get_minifigs(owned, wanted, query):
    params = {}
    if owned:
        params['owned'] = 1
    if wanted:
        params['wanted'] = 1
    if query:
        params['query'] = query
    minifigs_json = api.execute_api_request('getMinifigCollection', include_hash=True, params=params)
    for minifig in minifigs_json['minifigs']:
        print('{}: "{}" '.format(minifig['minifigNumber'], minifig['name']))


def update_minifig(id, owned, wanted):
    params = {}
    if owned is not None:
        if owned == 1:
            params['own'] = owned
        else:
            params['qtyOwned'] = owned
    if wanted is not None:
        params['want'] = 1 if wanted else 0
    api.execute_api_request('setMinifigCollection', include_hash=True, minifigNumber=id, params=params)
