from __future__ import print_function

import re
import sys

import api
import config

_VALID_SORTS = [
    'Number',
    'YearFrom',
    'YearFromDESC',
    'Pieces',
    'PiecesDESC',
    'Minifigs',
    'MinifigsDESC',
    'Rating',
    'UKRetailPrice',
    'UKRetailPriceDESC',
    'USRetailPrice',
    'USRetailPriceDESC',
    'CARetailPrice',
    'CARetailPriceDESC',
    'DERetailPrice',
    'DERetailPriceDESC',
    'FRRetailPrice',
    'FRRetailPriceDESC',
    'UKPricePerPiece',
    'UKPricePerPieceDESC',
    'USPricePerPiece',
    'USPricePerPieceDESC',
    'CAPricePerPiece',
    'CAPricePerPieceDESC',
    'DEPricePerPiece',
    'DEPricePerPieceDESC',
    'FRPricePerPiece',
    'FRPricePerPieceDESC',
    'Theme',
    'Subtheme',
    'Name',
    'Random',
    'QtyOwned',
    'QtyOwnedDESC',
    'OwnCount',
    'OwnCountDESC',
    'WantCount',
    'WantCountDESC',
    'UserRating'
    'CollectionID'
]


def get_sets(
        query,
        id,
        set_number,
        theme,
        subtheme,
        year,
        tag,
        owned,
        wanted,
        updated_since,
        limit,
        order_by,
        extended,
        id_only,
        count
):
    # NOTE: userHash is always required despite documentation saying it is optional unless using collection filters
    params = {}
    if query:
        params['query'] = query
    if id:
        params['setID'] = id
    if set_number:
        params['setNumber'] = ','.join(set_number)
    if theme:
        params['theme'] = ','.join(theme)
    if subtheme:
        params['subtheme'] = ','.join(subtheme)
    if year:
        params['year'] = ','.join(year)
    if tag:
        params['tag'] = tag
    if owned:
        params['owned'] = 1
    if wanted:
        params['wanted'] = 1
    if updated_since and _is_iso8601_date(updated_since):
        params['updatedSince'] = updated_since
    if order_by and _is_valid_order_by(order_by):
        params['orderBy'] = order_by
    if extended:
        params['extendedData'] = 1

    # TODO: validate limit
    if count:
        params['pageSize'] = 0
    else:
        params['pageSize'] = limit

    sets_json = api.execute_api_request('getSets', include_hash=True, params=params)
    config.update_cache(sets_json['sets'])
    if count:
        print(sets_json['matches'])
    else:
        [_print_set(lego_set, id_only) for lego_set in sets_json['sets']]


def update_set(id, owned, wanted, notes, rating):
    params = {}
    if owned is not None:
        if owned == 1:
            params['own'] = owned
        else:
            params['qtyOwned'] = owned
    if wanted is not None:
        params['want'] = 1 if wanted else 0
    if notes:
        params['notes'] = notes
    if rating is not None:
        params['rating'] = rating
    api.execute_api_request('setCollection', include_hash=True, setID=id, params=params)


def _id_to_set_number_generator(ids):
    for i in ids:
        yield _get_set_number(i)


def _set_number_to_id_generator(set_numbers):
    for n in set_numbers:
        yield _get_id(n)


def get_instructions(id, directory, set_number=None):
    ids = id if id is not None else _set_number_to_id_generator(set_number)
    set_numbers = set_number if set_number is not None else _id_to_set_number_generator(id)
    # for set_id in ids:
    for set_id, cur_set_number in zip(ids, set_numbers):
        # getting the set number will increase key usage and may result in hitting the API limit
        # cur_set_number = set_number if set_number is not None else _get_set_number(set_id)
        instructions_json = api.execute_api_request('getInstructions', setID=set_id)
        if not instructions_json['instructions']:
            print('No instructions found for {} ({})'.format(cur_set_number, set_id))
            if directory:
                with open('{}/{}_noinstructions.txt'.format(directory, cur_set_number), 'wb'):
                    pass  # don't actually write anything to the file
            continue

        instructions = instructions_json['instructions']
        if directory:
            [api.download_instruction(directory, cur_set_number, i) for i in instructions]
        else:
            [_print_instruction(cur_set_number, i) for i in instructions]


def get_themes(theme):
    themes_json = api.execute_api_request('getThemes')
    for a_theme in themes_json['themes']:
        if theme is None or re.search(theme, a_theme['theme'], flags=re.IGNORECASE):
            print('{} ({}-{}): {} set(s), {} subtheme(s)'.format(
                a_theme['theme'], a_theme['yearFrom'], a_theme['yearTo'], a_theme['setCount'], a_theme['subthemeCount']
            ))


def get_subthemes(theme, subtheme=None):
    subthemes_json = api.execute_api_request('getSubthemes', Theme=theme)
    for a_subtheme in subthemes_json['subthemes']:
        if subtheme is None or re.search(subtheme, a_subtheme['subtheme'], flags=re.IGNORECASE):
            print('{} ({}-{}): {} set(s)'.format(
                a_subtheme['subtheme'], a_subtheme['yearFrom'], a_subtheme['yearTo'], a_subtheme['setCount']
            ))


def get_years(theme):
    years_json = api.execute_api_request('getYears', Theme=theme)
    for year in years_json['years']:
        print('{}: {}'.format(year['year'], year['setCount']))


def _is_iso8601_date(updated_since):
    if not re.compile('^\\d{4}-\\d{2}-\\d{2}$').match(updated_since):
        sys.exit('ERROR: updated_since must have format yyyy-MM-dd')
    return True


def _print_set(lego_set, id_only):
    if id_only:
        print(lego_set['setID'])
        return

    collection_details = []
    if lego_set['collection']['owned']:
        collection_details.append(str(lego_set['collection']['qtyOwned']) + ' owned')
    if lego_set['collection']['wanted']:
        collection_details.append('wanted')

    set_details = '{}-{} {} {}'.format(
        lego_set['number'],
        lego_set['numberVariant'],
        lego_set['setID'],
        lego_set['name'].encode('UTF-8')
    )
    if collection_details:
        set_details = set_details + ' (' + ', '.join(collection_details) + ')'
    print(set_details)


def _is_valid_order_by(order_by):
    for valid_sort in _VALID_SORTS:
        if re.compile('^{}$'.format(valid_sort), flags=re.IGNORECASE).match(order_by):
            return True
    sys.exit('ERROR: invalid sort option')


def _get_set_number(set_id):
    cache = config.get_cache()
    if set_id not in cache['sets']:
        sets_json = api.execute_api_request('getSets', include_hash=True, params={'setID': set_id})
        config.update_cache(sets_json['sets'])
    return cache['sets'][set_id]


def _get_id(set_number):
    cache = config.get_cache()
    if set_number not in cache['sets']:
        sets_json = api.execute_api_request('getSets', include_hash=True, params={'setNumber': set_number})
        cache = config.update_cache(sets_json['sets'], cache)
    return cache['sets'][set_number]


def _print_instruction(set_number, instruction):
    print('{}: "{}" {}'.format(set_number, instruction['description'], instruction['URL']))
