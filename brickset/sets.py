import re
import sys
from dataclasses import dataclass
from typing import Any

from . import api
from . import cache


@dataclass
class SetFilters:
    query: str | None = None
    id: str | None = None
    set_number: list[str] | None = None
    theme: list[str] | None = None
    subtheme: list[str] | None = None
    year: list[str] | None = None
    tag: str | None = None
    owned: bool = False
    wanted: bool = False
    updated_since: str | None = None


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

_ISO_DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
_VALID_ORDER_BY_RE = re.compile('^(' + '|'.join(_VALID_SORTS) + ')$', re.IGNORECASE)


def get_sets(filters: SetFilters, limit: int, order_by: str | None, extended: bool, id_only: bool, count: bool) -> None:
    # NOTE: userHash is always required despite documentation saying it is optional unless using collection filters
    _validate_iso8601_date(filters.updated_since)
    _validate_order_by(order_by)
    _validate_limit(limit)

    params: dict[str, Any] = {k: v for k, v in {
        'query': filters.query,
        'setID': filters.id,
        'setNumber': ','.join(filters.set_number) if filters.set_number else None,
        'theme': ','.join(filters.theme) if filters.theme else None,
        'subtheme': ','.join(filters.subtheme) if filters.subtheme else None,
        'year': ','.join(filters.year) if filters.year else None,
        'tag': filters.tag,
        'owned': 1 if filters.owned else None,
        'wanted': 1 if filters.wanted else None,
        'updatedSince': filters.updated_since,
        'orderBy': order_by,
        'extendedData': 1 if extended else None,
        'pageSize': 0 if count else limit,
    }.items() if v is not None}
    sets_json = api.execute_api_request('getSets', include_hash=True, params=params)
    cache.update_cache(sets_json['sets'])
    if count:
        print(sets_json['matches'])
    else:
        for lego_set in sets_json['sets']:
            _print_set(lego_set, id_only)


def update_set(id: str, owned: int | None, wanted: bool | None, notes: str | None, rating: int | None) -> None:
    params: dict[str, Any] = {}
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


def get_themes(theme: str | None) -> None:
    themes_json = api.execute_api_request('getThemes')
    for a_theme in themes_json['themes']:
        if theme is None or re.search(theme, a_theme['theme'], flags=re.IGNORECASE):
            print(f'{a_theme["theme"]} ({a_theme["yearFrom"]}-{a_theme["yearTo"]}): {a_theme["setCount"]} set(s), {a_theme["subthemeCount"]} subtheme(s)')


def get_subthemes(theme: str, subtheme: str | None = None) -> None:
    subthemes_json = api.execute_api_request('getSubthemes', Theme=theme)
    for a_subtheme in subthemes_json['subthemes']:
        if subtheme is None or re.search(subtheme, a_subtheme['subtheme'], flags=re.IGNORECASE):
            print(f'{a_subtheme["subtheme"]} ({a_subtheme["yearFrom"]}-{a_subtheme["yearTo"]}): {a_subtheme["setCount"]} set(s)')


def get_years(theme: str) -> None:
    years_json = api.execute_api_request('getYears', Theme=theme)
    for year in years_json['years']:
        print(f'{year["year"]}: {year["setCount"]}')


def _print_set(lego_set: dict[str, Any], id_only: bool) -> None:
    if id_only:
        print(lego_set['setID'])
        return

    collection_details = []
    if lego_set['collection']['owned']:
        collection_details.append(f'{lego_set["collection"]["qtyOwned"]} owned')
    if lego_set['collection']['wanted']:
        collection_details.append('wanted')

    set_details = f'{lego_set["number"]}-{lego_set["numberVariant"]} {lego_set["setID"]} {lego_set["name"]}'
    if collection_details:
        set_details = f'{set_details} ({", ".join(collection_details)})'
    print(set_details)


def _validate_limit(limit: int | None) -> None:
    try:
        if limit is not None and not 1 <= int(limit) <= 500:
            sys.exit('ERROR: limit must be between 1 and 500')
    except (TypeError, ValueError):
        sys.exit('ERROR: limit must be an integer')


def _validate_iso8601_date(updated_since: str | None) -> None:
    if updated_since is not None and not _ISO_DATE_RE.match(updated_since):
        sys.exit('ERROR: updated_since must have format yyyy-MM-dd')


def _validate_order_by(order_by: str | None) -> None:
    if order_by is not None and not _VALID_ORDER_BY_RE.match(order_by):
        sys.exit('ERROR: invalid sort option')
