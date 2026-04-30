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
    print('TODO: update_minifig: id={} owned={}, wanted={}'.format(id, owned, wanted))
