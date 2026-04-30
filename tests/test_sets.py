import unittest
from unittest import mock

from brickset import sets


class TestSets(unittest.TestCase):

    @mock.patch('brickset.sets.config.update_cache')
    @mock.patch('builtins.print')
    @mock.patch('brickset.api.execute_api_request')
    def test_getSets(self, mock_api, mock_print, mock_update_cache):
        mock_api.return_value = {'sets': [], 'matches': 0}
        sets.get_sets(
            query='star wars', id=None, set_number=None, theme=None, subtheme=None,
            year=None, tag=None, owned=False, wanted=False, updated_since=None,
            limit=20, order_by=None, extended=False, id_only=False, count=False
        )
        mock_api.assert_called_once_with('getSets', include_hash=True, params={'query': 'star wars', 'pageSize': 20})

    def test_getSets_whenUpdatedSinceIsInvalid(self):
        with self.assertRaises(SystemExit) as cm:
            sets.get_sets(
                query=None, id=None, set_number=None, theme=None, subtheme=None,
                year=None, tag=None, owned=False, wanted=False, updated_since='not-a-date',
                limit=20, order_by=None, extended=False, id_only=False, count=False
            )
        self.assertEqual('ERROR: updated_since must have format yyyy-MM-dd', cm.exception.code)

    def test_getSets_whenOrderByIsInvalid(self):
        with self.assertRaises(SystemExit) as cm:
            sets.get_sets(
                query=None, id=None, set_number=None, theme=None, subtheme=None,
                year=None, tag=None, owned=False, wanted=False, updated_since=None,
                limit=20, order_by='Invalid', extended=False, id_only=False, count=False
            )
        self.assertEqual('ERROR: invalid sort option', cm.exception.code)

    def test_getSets_whenLimitIsInvalid(self):
        with self.assertRaises(SystemExit) as cm:
            sets.get_sets(
                query=None, id=None, set_number=None, theme=None, subtheme=None,
                year=None, tag=None, owned=False, wanted=False, updated_since=None,
                limit=501, order_by=None, extended=False, id_only=False, count=False
            )
        self.assertEqual('ERROR: limit must be between 1 and 500', cm.exception.code)

    @mock.patch('brickset.sets.config.update_cache')
    @mock.patch('builtins.print')
    @mock.patch('brickset.api.execute_api_request')
    def test_getSets_whenCountOnly(self, mock_api, mock_print, mock_update_cache):
        mock_api.return_value = {'sets': [], 'matches': 42}
        sets.get_sets(
            query='star wars', id=None, set_number=None, theme=None, subtheme=None,
            year=None, tag=None, owned=False, wanted=False, updated_since=None,
            limit=20, order_by=None, extended=False, id_only=False, count=True
        )
        mock_api.assert_called_once_with('getSets', include_hash=True, params={'query': 'star wars', 'pageSize': 0})
        mock_print.assert_called_once_with(42)

    @mock.patch('brickset.sets.config.update_cache')
    @mock.patch('builtins.print')
    @mock.patch('brickset.api.execute_api_request')
    def test_getSets_whenIdOnly(self, mock_api, mock_print, mock_update_cache):
        mock_api.return_value = {'sets': [{'setID': '789'}], 'matches': 1}
        sets.get_sets(
            query='star wars', id=None, set_number=None, theme=None, subtheme=None,
            year=None, tag=None, owned=False, wanted=False, updated_since=None,
            limit=20, order_by=None, extended=False, id_only=True, count=False
        )
        mock_print.assert_called_once_with('789')

    @mock.patch('brickset.sets.config.update_cache', return_value={'sets': {'123': '456-1', '456-1': '123'}})
    @mock.patch('brickset.sets.config.get_cache', return_value={'sets': {}})
    @mock.patch('builtins.print')
    @mock.patch('brickset.api.execute_api_request')
    def test_getInstructions(self, mock_api, mock_print, mock_get_cache, mock_update_cache):
        get_sets_response = {'sets': [{'number': '456', 'numberVariant': 1, 'setID': '123'}]}
        get_instructions_response = {
            'status': 'success',
            'matches': 2,
            'instructions': [
                {'URL': 'https://www.lego.com/biassets/bi/6307466.pdf', 'description': 'BI 2002/ 2 - 30453 V29'},
                {'URL': 'https://www.lego.com/biassets/bi/6307469.pdf', 'description': 'BI 2002/ 2 - 30453 V39'}
            ]
        }
        mock_api.side_effect = [get_sets_response, get_instructions_response]

        sets.get_instructions(['123'], None, None)

        mock_api.assert_has_calls([
            mock.call('getSets', include_hash=True, params={'setID': '123'}),
            mock.call('getInstructions', setID='123')
        ])
        mock_print.assert_has_calls([
            mock.call('456-1: "BI 2002/ 2 - 30453 V29" https://www.lego.com/biassets/bi/6307466.pdf'),
            mock.call('456-1: "BI 2002/ 2 - 30453 V39" https://www.lego.com/biassets/bi/6307469.pdf'),
        ])

    @mock.patch('brickset.sets.config.update_cache', return_value={'sets': {'123': '456-1', '456-1': '123'}})
    @mock.patch('brickset.sets.config.get_cache', return_value={'sets': {}})
    @mock.patch('builtins.print')
    @mock.patch('brickset.api.execute_api_request')
    def test_getInstructions_whenNoInstructionsExist(self, mock_api, mock_print, mock_get_cache, mock_update_cache):
        get_sets_response = {'sets': [{'number': '456', 'numberVariant': 1, 'setID': '123'}]}
        get_instructions_response = {'status': 'success', 'matches': 0, 'instructions': []}
        mock_api.side_effect = [get_sets_response, get_instructions_response]

        sets.get_instructions(['123'], None, None)

        mock_api.assert_has_calls([
            mock.call('getSets', include_hash=True, params={'setID': '123'}),
            mock.call('getInstructions', setID='123')
        ])
        mock_print.assert_called_once_with('No instructions found for 456-1 (123)')

    @mock.patch('brickset.sets.config.update_cache', return_value={'sets': {'123': '456-1', '456-1': '123'}})
    @mock.patch('brickset.sets.config.get_cache', return_value={'sets': {}})
    @mock.patch('brickset.api.download_instruction')
    @mock.patch('brickset.api.execute_api_request')
    def test_getInstructions_whenDownloading(self, mock_api, mock_download, mock_get_cache, mock_update_cache):
        get_sets_response = {'sets': [{'number': '456', 'numberVariant': 1, 'setID': '123'}]}
        get_instructions_response = {
            'status': 'success',
            'matches': 2,
            'instructions': [
                {'URL': 'https://www.lego.com/biassets/bi/6307466.pdf', 'description': 'BI 2002/ 2 - 30453 V29'},
                {'URL': 'https://www.lego.com/biassets/bi/6307469.pdf', 'description': 'BI 2002/ 2 - 30453 V39'}
            ]
        }
        mock_api.side_effect = [get_sets_response, get_instructions_response]

        sets.get_instructions(['123'], '/tmp', None)

        mock_api.assert_has_calls([
            mock.call('getSets', include_hash=True, params={'setID': '123'}),
            mock.call('getInstructions', setID='123')
        ])
        mock_download.assert_has_calls([
            mock.call('/tmp', '456-1', get_instructions_response['instructions'][0]),
            mock.call('/tmp', '456-1', get_instructions_response['instructions'][1])
        ])

    @mock.patch('brickset.api.download_instruction')
    @mock.patch('brickset.api.execute_api_request')
    def test_getInstructions_whenDownloadingAndSetNumberSupplied(self, mock_api, mock_download):
        get_instructions_response = {
            'status': 'success',
            'matches': 2,
            'instructions': [
                {'URL': 'https://www.lego.com/biassets/bi/6307466.pdf', 'description': 'BI 2002/ 2 - 30453 V29'},
                {'URL': 'https://www.lego.com/biassets/bi/6307469.pdf', 'description': 'BI 2002/ 2 - 30453 V39'}
            ]
        }
        mock_api.return_value = get_instructions_response

        sets.get_instructions(['123'], '/tmp', ['SET_NUM'])

        mock_api.assert_called_once_with('getInstructions', setID='123')
        mock_download.assert_has_calls([
            mock.call('/tmp', 'SET_NUM', get_instructions_response['instructions'][0]),
            mock.call('/tmp', 'SET_NUM', get_instructions_response['instructions'][1])
        ])

    @mock.patch('builtins.open', mock.mock_open())
    @mock.patch('brickset.sets.config.update_cache', return_value={'sets': {'123': '456-1', '456-1': '123'}})
    @mock.patch('brickset.sets.config.get_cache', return_value={'sets': {}})
    @mock.patch('builtins.print')
    @mock.patch('brickset.api.execute_api_request')
    def test_getInstructions_whenDownloadingAndNoInstructionsExist(self, mock_api, mock_print, mock_get_cache, mock_update_cache):
        get_sets_response = {'sets': [{'number': '456', 'numberVariant': 1, 'setID': '123'}]}
        get_instructions_response = {'status': 'success', 'matches': 0, 'instructions': []}
        mock_api.side_effect = [get_sets_response, get_instructions_response]

        with mock.patch('builtins.open', mock.mock_open()) as mock_open:
            sets.get_instructions(['123'], '/tmp', None)

        mock_api.assert_has_calls([
            mock.call('getSets', include_hash=True, params={'setID': '123'}),
            mock.call('getInstructions', setID='123')
        ])
        mock_print.assert_called_once_with('No instructions found for 456-1 (123)')
        mock_open.assert_called_once_with('/tmp/456-1_noinstructions.txt', 'wb')

    @mock.patch('brickset.sets.config.update_cache', return_value={'sets': {'1394': '3219-1', '3219-1': '1394'}})
    @mock.patch('brickset.sets.config.get_cache', return_value={'sets': {}})
    @mock.patch('brickset.api.execute_api_request')
    def test__getSetNumber(self, mock_api, mock_get_cache, mock_update_cache):
        mock_api.return_value = {
            'status': 'success',
            'matches': 1,
            'sets': [{'setID': 1394, 'number': '3219', 'numberVariant': 1}]
        }

        set_number = sets._get_set_number('1394')

        mock_api.assert_called_once_with('getSets', include_hash=True, params={'setID': '1394'})
        self.assertEqual('3219-1', set_number)

    @mock.patch('builtins.print')
    def test_getThemes(self, mock_print):
        with mock.patch('brickset.api.execute_api_request') as mock_api:
            mock_api.return_value = {
                'status': 'success',
                'matches': 2,
                'themes': [
                    {'theme': '4 Juniors', 'setCount': 24, 'subthemeCount': 5, 'yearFrom': 2003, 'yearTo': 2004},
                    {'theme': 'Action Wheelers', 'setCount': 9, 'subthemeCount': 0, 'yearFrom': 2000, 'yearTo': 2001}
                ]
            }
            sets.get_themes(None)
        mock_print.assert_has_calls([
            mock.call('4 Juniors (2003-2004): 24 set(s), 5 subtheme(s)'),
            mock.call('Action Wheelers (2000-2001): 9 set(s), 0 subtheme(s)')
        ])

    @mock.patch('builtins.print')
    def test_getThemes_withThemeFilter(self, mock_print):
        with mock.patch('brickset.api.execute_api_request') as mock_api:
            mock_api.return_value = {
                'status': 'success',
                'matches': 2,
                'themes': [
                    {'theme': '4 Juniors', 'setCount': 24, 'subthemeCount': 5, 'yearFrom': 2003, 'yearTo': 2004},
                    {'theme': 'Action Wheelers', 'setCount': 9, 'subthemeCount': 0, 'yearFrom': 2000, 'yearTo': 2001}
                ]
            }
            sets.get_themes('Wheelers')
        mock_print.assert_called_once_with('Action Wheelers (2000-2001): 9 set(s), 0 subtheme(s)')

    @mock.patch('builtins.print')
    def test_getSubthemes(self, mock_print):
        with mock.patch('brickset.api.execute_api_request') as mock_api:
            mock_api.return_value = {
                'status': 'success',
                'matches': 2,
                'subthemes': [
                    {'theme': 'Star Wars', 'subtheme': '{None}', 'setCount': 3, 'yearFrom': 2019, 'yearTo': 2019},
                    {'theme': 'Star Wars', 'subtheme': '4 Plus', 'setCount': 4, 'yearFrom': 2019, 'yearTo': 2020}
                ]
            }
            sets.get_subthemes('Star Wars', None)
        mock_print.assert_has_calls([
            mock.call('{None} (2019-2019): 3 set(s)'),
            mock.call('4 Plus (2019-2020): 4 set(s)'),
        ])

    @mock.patch('builtins.print')
    def test_getSubthemes_withSubthemeFilter(self, mock_print):
        with mock.patch('brickset.api.execute_api_request') as mock_api:
            mock_api.return_value = {
                'status': 'success',
                'matches': 2,
                'subthemes': [
                    {'theme': 'Star Wars', 'subtheme': '{None}', 'setCount': 3, 'yearFrom': 2019, 'yearTo': 2019},
                    {'theme': 'Star Wars', 'subtheme': '4 Plus', 'setCount': 4, 'yearFrom': 2019, 'yearTo': 2020}
                ]
            }
            sets.get_subthemes('Star Wars', '4 Plus')
        mock_print.assert_called_once_with('4 Plus (2019-2020): 4 set(s)')

    @mock.patch('builtins.print')
    def test_getYears(self, mock_print):
        with mock.patch('brickset.api.execute_api_request') as mock_api:
            mock_api.return_value = {
                'status': 'success',
                'matches': 16,
                'years': [
                    {'theme': 'City', 'year': '2005', 'setCount': 46},
                    {'theme': 'City', 'year': '2006', 'setCount': 34}
                ]
            }
            sets.get_years('City')
        mock_print.assert_has_calls([
            mock.call('2005: 46'),
            mock.call('2006: 34')
        ])

    def test__isValidLimit_whenValid(self):
        self.assertTrue(sets._is_valid_limit(1))
        self.assertTrue(sets._is_valid_limit(20))
        self.assertTrue(sets._is_valid_limit(500))

    def test__isValidLimit_whenAboveMax(self):
        with self.assertRaises(SystemExit) as cm:
            sets._is_valid_limit(501)
        self.assertEqual('ERROR: limit must be between 1 and 500', cm.exception.code)

    def test__isValidLimit_whenBelowMin(self):
        with self.assertRaises(SystemExit) as cm:
            sets._is_valid_limit(0)
        self.assertEqual('ERROR: limit must be between 1 and 500', cm.exception.code)

    def test__isValidLimit_whenNotAnInteger(self):
        with self.assertRaises(SystemExit) as cm:
            sets._is_valid_limit('abc')
        self.assertEqual('ERROR: limit must be an integer', cm.exception.code)

    def test__isIso8601Date_whenValid(self):
        self.assertTrue(sets._is_iso8601_date('2020-05-05'))

    def test__isIso8601Date_whenInvalid(self):
        with self.assertRaises(SystemExit) as cm:
            sets._is_iso8601_date('May 5, 2020')
        self.assertEqual('ERROR: updated_since must have format yyyy-MM-dd', cm.exception.code)

    @mock.patch('builtins.print')
    def test__printSet(self, mock_print):
        lego_set = {
            'number': '123',
            'numberVariant': '4',
            'setID': '789',
            'name': 'Set A',
            'collection': {'owned': False, 'wanted': False}
        }
        sets._print_set(lego_set, False)
        mock_print.assert_called_once_with('123-4 789 Set A')

    @mock.patch('builtins.print')
    def test__printSet_idOnly(self, mock_print):
        sets._print_set({'setID': '789'}, True)
        mock_print.assert_called_once_with('789')

    def test__isValidOrderBy_whenValid(self):
        self.assertTrue(sets._is_valid_order_by('YearFromDESC'))
        self.assertTrue(sets._is_valid_order_by('yearfromdesc'))

    def test__isValidOrderBy_whenInvalid(self):
        with self.assertRaises(SystemExit) as cm:
            sets._is_valid_order_by('ThemeDESC')
        self.assertEqual('ERROR: invalid sort option', cm.exception.code)

    @mock.patch('builtins.print')
    def test__printInstruction(self, mock_print):
        sets._print_instruction('123-4', {'URL': 'lego.com/123-4.pdf', 'description': '123-4 instructions'})
        mock_print.assert_called_once_with('123-4: "123-4 instructions" lego.com/123-4.pdf')