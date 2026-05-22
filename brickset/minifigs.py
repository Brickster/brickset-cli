from __future__ import annotations

from typing import Any

from . import api


def get_minifigs(owned: bool, wanted: bool, query: str | None) -> None:
    params: dict[str, Any] = {}
    if owned:
        params['owned'] = 1
    if wanted:
        params['wanted'] = 1
    if query:
        params['query'] = query
    minifigs_json = api.execute_api_request('getMinifigCollection', include_hash=True, params=params)
    for minifig in minifigs_json['minifigs']:
        print(f'{minifig["minifigNumber"]}: "{minifig["name"]}" ')


def update_minifig(id: str, owned: int | None, wanted: bool | None) -> None:
    params = {}
    if owned is not None:
        if owned == 1:
            params['own'] = owned
        else:
            params['qtyOwned'] = owned
    if wanted is not None:
        params['want'] = 1 if wanted else 0
    api.execute_api_request('setMinifigCollection', include_hash=True, minifigNumber=id, params=params)
