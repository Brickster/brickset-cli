import unittest
from unittest import mock

from brickset import api


class TestApi(unittest.TestCase):

    @mock.patch('brickset.api.requests.get')
    @mock.patch('brickset.api.config.get_config', return_value={'api_key': 'test-key'})
    def test_executeApiRequest(self, mock_config, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'status': 'success', 'sets': []}

        result = api.execute_api_request('getSets')

        mock_get.assert_called_once_with(
            'https://brickset.com/api/v3.asmx/getSets',
            params={'apiKey': 'test-key'}
        )
        self.assertEqual({'status': 'success', 'sets': []}, result)

    @mock.patch('brickset.api.requests.get')
    @mock.patch('brickset.api.config.get_config', return_value={'api_key': 'test-key', 'hash': 'user-hash'})
    def test_executeApiRequest_withHash(self, mock_config, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'status': 'success', 'sets': []}

        api.execute_api_request('getSets', include_hash=True)

        mock_get.assert_called_once_with(
            'https://brickset.com/api/v3.asmx/getSets',
            params={'apiKey': 'test-key', 'userHash': 'user-hash'}
        )

    @mock.patch('brickset.api.config.get_config', return_value={'api_key': 'test-key'})
    def test_executeApiRequest_whenHashRequiredButMissing(self, mock_config):
        with self.assertRaises(SystemExit) as cm:
            api.execute_api_request('getSets', include_hash=True)
        self.assertEqual('ERROR: user hash required. Run: brickset login', cm.exception.code)

    @mock.patch('brickset.api.requests.get')
    @mock.patch('brickset.api.config.get_config', return_value={'api_key': 'test-key'})
    def test_executeApiRequest_whenNon200Response(self, mock_config, mock_get):
        mock_get.return_value.status_code = 500
        mock_get.return_value.text = 'Internal Server Error'

        with self.assertRaises(SystemExit) as cm:
            api.execute_api_request('getSets')
        self.assertEqual('ERROR: getSets API returned an unexpected error', cm.exception.code)

    @mock.patch('brickset.api.requests.get')
    @mock.patch('brickset.api.config.get_config', return_value={'api_key': 'test-key'})
    def test_executeApiRequest_whenErrorStatus(self, mock_config, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'status': 'error', 'message': 'Invalid key'}
        mock_get.return_value.text = '{"status": "error", "message": "Invalid key"}'

        with self.assertRaises(SystemExit) as cm:
            api.execute_api_request('getSets')
        self.assertEqual('ERROR: getSets API returned an unexpected error', cm.exception.code)
