import json
import unittest
from unittest import mock

from brickset import cache


class TestCache(unittest.TestCase):

    @mock.patch('pathlib.Path.exists', return_value=False)
    def test_getCache_whenNoCacheExists(self, mock_exists):
        result = cache.get_cache()
        self.assertEqual({'sets': {}}, result)

    @mock.patch('pathlib.Path.exists', return_value=True)
    def test_getCache(self, mock_exists):
        cache_data = {'sets': {'123': '456-1', '456-1': '123'}}
        with mock.patch('builtins.open', mock.mock_open(read_data=json.dumps(cache_data))):
            result = cache.get_cache()
        self.assertEqual(cache_data, result)

    def test_saveCache(self):
        mock_open = mock.mock_open()
        with mock.patch('builtins.open', mock_open):
            cache.save_cache({'sets': {}})
        mock_open.assert_called_once_with(mock.ANY, 'w')
        written = ''.join(c.args[0] for c in mock_open().write.call_args_list)
        self.assertEqual(json.dumps({'sets': {}}, indent=2), written)

    @mock.patch('brickset.cache.save_cache')
    @mock.patch('brickset.cache.get_cache', return_value={'sets': {}})
    def test_updateCache(self, mock_get_cache, mock_save_cache):
        sets = [{'setID': '123', 'number': '456', 'numberVariant': 1}]
        result = cache.update_cache(sets)
        self.assertEqual({'sets': {'123': '456-1', '456-1': '123'}}, result)
        mock_save_cache.assert_called_once_with({'sets': {'123': '456-1', '456-1': '123'}})

    @mock.patch('brickset.cache.save_cache')
    def test_updateCache_withExistingCache(self, mock_save_cache):
        existing = {'sets': {'999': '888-1', '888-1': '999'}}
        sets = [{'setID': '123', 'number': '456', 'numberVariant': 1}]
        result = cache.update_cache(sets, existing)
        self.assertEqual({
            'sets': {'999': '888-1', '888-1': '999', '123': '456-1', '456-1': '123'}
        }, result)

    @mock.patch('brickset.cache.update_cache', return_value={'sets': {'123': '456-1', '456-1': '123'}})
    @mock.patch('brickset.cache.api.execute_api_request', return_value={'sets': []})
    @mock.patch('brickset.cache.get_cache', return_value={'sets': {}})
    def test_getSetNumber_whenCacheMiss(self, mock_get_cache, mock_api, mock_update_cache):
        cache._get_set_number('123')
        mock_api.assert_called_once_with('getSets', include_hash=True, params={'setID': '123'})

    @mock.patch('brickset.cache.get_cache', return_value={'sets': {'123': '456-1', '456-1': '123'}})
    def test_getSetNumber_whenCacheHit(self, mock_get_cache):
        self.assertEqual('456-1', cache._get_set_number('123'))

    @mock.patch('brickset.cache.update_cache', return_value={'sets': {'123': '456-1', '456-1': '123'}})
    @mock.patch('brickset.cache.api.execute_api_request', return_value={'sets': []})
    @mock.patch('brickset.cache.get_cache', return_value={'sets': {}})
    def test_getId_whenCacheMiss(self, mock_get_cache, mock_api, mock_update_cache):
        cache._get_id('456-1')
        mock_api.assert_called_once_with('getSets', include_hash=True, params={'setNumber': '456-1'})

    @mock.patch('brickset.cache.get_cache', return_value={'sets': {'123': '456-1', '456-1': '123'}})
    def test_getId_whenCacheHit(self, mock_get_cache):
        self.assertEqual('123', cache._get_id('456-1'))

    @mock.patch('brickset.cache.get_cache', return_value={'sets': {'123': '456-1', '456-1': '123'}})
    def test_idToSetNumberGenerator(self, mock_get_cache):
        self.assertEqual(['456-1', '456-1'], list(cache.id_to_set_number_generator(['123', '123'])))

    @mock.patch('brickset.cache.get_cache', return_value={'sets': {'123': '456-1', '456-1': '123'}})
    def test_setNumberToIdGenerator(self, mock_get_cache):
        self.assertEqual(['123', '123'], list(cache.set_number_to_id_generator(['456-1', '456-1'])))
