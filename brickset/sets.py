from __future__ import print_function

import re
import sys

from . import api
from . import cache

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
    'UserRating',
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

    if count:
        params['pageSize'] = 0
    else:
        if not _is_valid_limit(limit):
            return
        params['pageSize'] = limit

    sets_json = api.execute_api_request('getSets', include_hash=True, params=params)
    cache.update_cache(sets_json['sets'])
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


def _is_valid_limit(limit):
    try:
        if not 1 <= int(limit) <= 500:
            sys.exit('ERROR: limit must be between 1 and 500')
    except (TypeError, ValueError):
        sys.exit('ERROR: limit must be an integer')
    return True


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
        lego_set['name']
    )
    if collection_details:
        set_details = set_details + ' (' + ', '.join(collection_details) + ')'
    print(set_details)


def _is_valid_order_by(order_by):
    for valid_sort in _VALID_SORTS:
        if re.compile('^{}$'.format(valid_sort), flags=re.IGNORECASE).match(order_by):
            return True
    sys.exit('ERROR: invalid sort option')
