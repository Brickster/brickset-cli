from __future__ import print_function

import api


def get_minifigs(owned, wanted, query):
    # {"status":"success","matches":576,"minifigs":[
    #   {
    #     "minifigNumber": "47205pb025",
    #     "name": "Duplo Figure Lego Ville, Child Boy, Blue Legs, White Top with Blue Overalls, Lime Cap, Freckles",
    #     "category": "Duplo / General",
    #     "ownedInSets": 1,
    #     "ownedLoose": 0,
    #     "ownedTotal": 1,
    #     "wanted": false
    #   }
    # print('get_minifigs: owned={}, wanted={}, query={}'.format(owned, wanted, query))
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
    print('update_minifig: id={} owned={}, wanted={}'.format(id, owned, wanted))
