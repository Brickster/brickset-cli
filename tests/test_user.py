import unittest
from unittest import mock

from brickset import user


class TestUser(unittest.TestCase):

    @mock.patch('builtins.print')
    @mock.patch('brickset.user.api.execute_api_request')
    def test_showUsage_all(self, mock_api, mock_print):
        mock_api.return_value = {
            'apiKeyUsage': [
                {'dateStamp': '2024-01-02T00:00:00Z', 'count': 10},
                {'dateStamp': '2024-01-01T00:00:00Z', 'count': 5},
            ]
        }
        user.show_usage('ALL')
        mock_print.assert_has_calls([
            mock.call('2024-01-02T00:00:00Z: 10'),
            mock.call('2024-01-01T00:00:00Z: 5'),
        ])

    @mock.patch('builtins.print')
    @mock.patch('brickset.user.api.execute_api_request')
    def test_showUsage_today(self, mock_api, mock_print):
        today = '2024-01-02T00:00:00Z'
        mock_api.return_value = {'apiKeyUsage': [{'dateStamp': today, 'count': 10}]}
        with mock.patch('brickset.user.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = today
            user.show_usage('TODAY')
        mock_print.assert_called_once_with('2024-01-02T00:00:00Z: 10')

    @mock.patch('builtins.print')
    @mock.patch('brickset.user.api.execute_api_request')
    def test_showUsage_today_whenNoUsageToday(self, mock_api, mock_print):
        mock_api.return_value = {'apiKeyUsage': [{'dateStamp': '2024-01-01T00:00:00Z', 'count': 5}]}
        with mock.patch('brickset.user.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = '2024-01-02T00:00:00Z'
            user.show_usage('TODAY')
        mock_print.assert_called_once_with('2024-01-02T00:00:00Z: 0')

    @mock.patch('builtins.print')
    @mock.patch('brickset.user.api.execute_api_request')
    def test_showUsage_last(self, mock_api, mock_print):
        mock_api.return_value = {'apiKeyUsage': [{'dateStamp': '2024-01-01T00:00:00Z', 'count': 5}]}
        user.show_usage('LAST')
        mock_print.assert_called_once_with('2024-01-01T00:00:00Z: 5')

    @mock.patch('builtins.print')
    @mock.patch('brickset.user.api.execute_api_request')
    def test_showUsage_today_whenEmptyUsage(self, mock_api, mock_print):
        mock_api.return_value = {'apiKeyUsage': []}
        user.show_usage('TODAY')
        mock_print.assert_not_called()

    @mock.patch('brickset.user._config_directory', return_value='/tmp/')
    @mock.patch('brickset.user.get_config', return_value={'api_key': 'test-key'})
    @mock.patch('brickset.user.api.execute_api_request', return_value={'hash': 'user-hash-123'})
    @mock.patch('getpass.getpass', return_value='testpass')
    @mock.patch('builtins.input', return_value='testuser')
    def test_logIn(self, mock_input, mock_getpass, mock_api, mock_get_config, mock_config_dir):
        with mock.patch('builtins.open', mock.mock_open()) as mock_open:
            user.log_in()

        mock_api.assert_called_once_with('login', username='testuser', password='testpass')
        mock_open.assert_called_once_with('/tmp/config', 'w')
        handle = mock_open()
        written = ''.join(call.args[0] for call in handle.write.call_args_list)
        self.assertIn('user-hash-123', written)
