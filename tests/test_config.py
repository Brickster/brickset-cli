import json
import unittest
from pathlib import Path
from unittest import mock

from brickset import config


class TestConfig(unittest.TestCase):

    def test_configDirectory_whenBricksetDirSet(self):
        with mock.patch.dict('os.environ', {'BRICKSET_DIR': '/custom/path'}):
            self.assertEqual(Path('/custom/path'), config._config_directory())

    @mock.patch('pathlib.Path.exists', return_value=True)
    def test_getConfig(self, mock_exists):
        mock_open = mock.mock_open(read_data=json.dumps({'api_key': 'abc123'}))
        with mock.patch('builtins.open', mock_open):
            result = config.get_config()
        self.assertEqual({'api_key': 'abc123'}, result)

    @mock.patch('pathlib.Path.exists', return_value=False)
    def test_getConfig_whenNoConfigExists(self, mock_exists):
        with self.assertRaises(SystemExit) as cm:
            config.get_config()
        self.assertEqual('ERROR: no config exists. Run: brickset config API_KEY', cm.exception.code)

    @mock.patch('pathlib.Path.exists', return_value=True)
    def test_configure(self, mock_exists):
        mock_open = mock.mock_open()
        with mock.patch('builtins.open', mock_open):
            config.configure('abc123')
        mock_open.assert_called_once_with(mock.ANY, 'w')
        written = ''.join(c.args[0] for c in mock_open().write.call_args_list)
        self.assertEqual(json.dumps({'api_key': 'abc123'}), written)

    @mock.patch('pathlib.Path.mkdir')
    @mock.patch('pathlib.Path.exists', return_value=False)
    def test_configure_whenDirectoryDoesNotExist(self, mock_exists, mock_mkdir):
        with mock.patch('builtins.open', mock.mock_open()):
            config.configure('abc123')
        mock_mkdir.assert_called_once()
