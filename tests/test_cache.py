import json
import unittest
from unittest import mock

from brickset import cache


class TestCache(unittest.TestCase):

    @mock.patch('os.path.exists', return_value=False)
    def test_getCache_whenNoCacheExists(self, mock_exists):
        result = cache.get_cache()
        self.assertEqual({'sets': {}}, result)

    @mock.patch('os.path.exists', return_value=True)
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
