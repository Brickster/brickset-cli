import json
import unittest
from unittest import mock

from brickset import config


class TestConfig(unittest.TestCase):

    @mock.patch('builtins.open', mock.mock_open())
    @mock.patch('os.path.exists', return_value=True)
    def test_getConfig(self, mock_exists):
        mock_open = mock.mock_open(read_data=json.dumps({'api_key': 'abc123'}))
        with mock.patch('builtins.open', mock_open):
            result = config.get_config()
        self.assertEqual({'api_key': 'abc123'}, result)

    @mock.patch('os.path.exists', return_value=False)
    def test_getConfig_whenNoConfigExists(self, mock_exists):
        with self.assertRaises(SystemExit) as cm:
            config.get_config()
        self.assertEqual('ERROR: no config exists. Run: brickset config API_KEY', cm.exception.code)

    @mock.patch('os.path.exists', return_value=True)
    def test_configure(self, mock_exists):
        mock_open = mock.mock_open()
        with mock.patch('builtins.open', mock_open):
            config.configure('abc123')
        mock_open.assert_called_once_with(mock.ANY, 'w')
        written = ''.join(c.args[0] for c in mock_open().write.call_args_list)
        self.assertEqual(json.dumps({'api_key': 'abc123'}), written)

    @mock.patch('os.mkdir')
    @mock.patch('os.path.exists', return_value=False)
    def test_configure_whenDirectoryDoesNotExist(self, mock_exists, mock_mkdir):
        with mock.patch('builtins.open', mock.mock_open()):
            config.configure('abc123')
        mock_mkdir.assert_called_once()

    @mock.patch('os.path.exists', return_value=False)
    def test_getCache_whenNoCacheExists(self, mock_exists):
        result = config.get_cache()
        self.assertEqual({'sets': {}}, result)

    @mock.patch('os.path.exists', return_value=True)
    def test_getCache(self, mock_exists):
        cache_data = {'sets': {'123': '456-1', '456-1': '123'}}
        with mock.patch('builtins.open', mock.mock_open(read_data=json.dumps(cache_data))):
            result = config.get_cache()
        self.assertEqual(cache_data, result)

    def test_saveCache(self):
        mock_open = mock.mock_open()
        with mock.patch('builtins.open', mock_open):
            config.save_cache({'sets': {}})
        mock_open.assert_called_once_with(mock.ANY, 'w')
        written = ''.join(c.args[0] for c in mock_open().write.call_args_list)
        self.assertEqual(json.dumps({'sets': {}}, indent=2), written)

    @mock.patch('brickset.config.save_cache')
    @mock.patch('brickset.config.get_cache', return_value={'sets': {}})
    def test_updateCache(self, mock_get_cache, mock_save_cache):
        sets = [{'setID': '123', 'number': '456', 'numberVariant': 1}]
        result = config.update_cache(sets)
        self.assertEqual({'sets': {'123': '456-1', '456-1': '123'}}, result)
        mock_save_cache.assert_called_once_with({'sets': {'123': '456-1', '456-1': '123'}})

    @mock.patch('brickset.config.save_cache')
    def test_updateCache_withExistingCache(self, mock_save_cache):
        existing = {'sets': {'999': '888-1', '888-1': '999'}}
        sets = [{'setID': '123', 'number': '456', 'numberVariant': 1}]
        result = config.update_cache(sets, existing)
        self.assertEqual({
            'sets': {'999': '888-1', '888-1': '999', '123': '456-1', '456-1': '123'}
        }, result)

    @unittest.skip('log_in requires interactive input (input + getpass) and writes to disk — needs refactor to be testable')
    def test_logIn(self):
        pass

    @mock.patch('builtins.print')
    @mock.patch('brickset.config.api.execute_api_request')
    def test_showUsage_all(self, mock_api, mock_print):
        mock_api.return_value = {
            'apiKeyUsage': [
                {'dateStamp': '2024-01-02T00:00:00Z', 'count': 10},
                {'dateStamp': '2024-01-01T00:00:00Z', 'count': 5},
            ]
        }
        config.show_usage('ALL')
        mock_print.assert_has_calls([
            mock.call('2024-01-02T00:00:00Z: 10'),
            mock.call('2024-01-01T00:00:00Z: 5'),
        ])

    @mock.patch('builtins.print')
    @mock.patch('brickset.config.api.execute_api_request')
    def test_showUsage_today(self, mock_api, mock_print):
        today = '2024-01-02T00:00:00Z'
        mock_api.return_value = {'apiKeyUsage': [{'dateStamp': today, 'count': 10}]}
        with mock.patch('brickset.config.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = today
            config.show_usage('TODAY')
        mock_print.assert_called_once_with('2024-01-02T00:00:00Z: 10')

    @mock.patch('builtins.print')
    @mock.patch('brickset.config.api.execute_api_request')
    def test_showUsage_today_whenNoUsageToday(self, mock_api, mock_print):
        mock_api.return_value = {'apiKeyUsage': [{'dateStamp': '2024-01-01T00:00:00Z', 'count': 5}]}
        with mock.patch('brickset.config.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = '2024-01-02T00:00:00Z'
            config.show_usage('TODAY')
        mock_print.assert_called_once_with('2024-01-02T00:00:00Z: 0')

    @mock.patch('builtins.print')
    @mock.patch('brickset.config.api.execute_api_request')
    def test_showUsage_last(self, mock_api, mock_print):
        mock_api.return_value = {'apiKeyUsage': [{'dateStamp': '2024-01-01T00:00:00Z', 'count': 5}]}
        config.show_usage('LAST')
        mock_print.assert_called_once_with('2024-01-01T00:00:00Z: 5')