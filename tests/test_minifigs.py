import unittest
from unittest import mock

from brickset import minifigs


class TestMinifigs(unittest.TestCase):

    @mock.patch('builtins.print')
    @mock.patch('brickset.api.execute_api_request')
    def test_getMinifigs(self, mock_api, mock_print):
        mock_api.return_value = {
            'minifigs': [
                {'minifigNumber': 'sw0001', 'name': 'Darth Vader'},
                {'minifigNumber': 'sw0002', 'name': 'Luke Skywalker'},
            ]
        }

        minifigs.get_minifigs(owned=False, wanted=False, query=None)

        mock_api.assert_called_once_with('getMinifigCollection', include_hash=True, params={})
        mock_print.assert_has_calls([
            mock.call('sw0001: "Darth Vader" '),
            mock.call('sw0002: "Luke Skywalker" '),
        ])

    @mock.patch('builtins.print')
    @mock.patch('brickset.api.execute_api_request')
    def test_getMinifigs_whenOwned(self, mock_api, mock_print):
        mock_api.return_value = {'minifigs': []}

        minifigs.get_minifigs(owned=True, wanted=False, query=None)

        mock_api.assert_called_once_with('getMinifigCollection', include_hash=True, params={'owned': 1})

    @mock.patch('builtins.print')
    @mock.patch('brickset.api.execute_api_request')
    def test_getMinifigs_whenWanted(self, mock_api, mock_print):
        mock_api.return_value = {'minifigs': []}

        minifigs.get_minifigs(owned=False, wanted=True, query=None)

        mock_api.assert_called_once_with('getMinifigCollection', include_hash=True, params={'wanted': 1})

    @mock.patch('builtins.print')
    @mock.patch('brickset.api.execute_api_request')
    def test_getMinifigs_whenQuery(self, mock_api, mock_print):
        mock_api.return_value = {'minifigs': []}

        minifigs.get_minifigs(owned=False, wanted=False, query='vader')

        mock_api.assert_called_once_with('getMinifigCollection', include_hash=True, params={'query': 'vader'})

    @unittest.skip('not implemented')
    def test_updateMinifig(self):
        pass