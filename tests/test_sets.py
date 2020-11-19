import mock
import unittest

import bin.sets as sets


class TestSets(unittest.TestCase):

    @mock.patch('__builtin__.print')
    def test_getSets(self, mock_print):
        self.fail('not implemented')

    @mock.patch('__builtin__.print')
    def test_getSets_whenUpdatedSinceIsInvalid(self, mock_print):
        self.fail('not implemented')

    @mock.patch('__builtin__.print')
    def test_getSets_whenOrderByIsInvalid(self, mock_print):
        self.fail('not implemented')

    @mock.patch('__builtin__.print')
    def test_getSets_whenLimitIsInvalid(self, mock_print):
        self.fail('not implemented')

    @mock.patch('__builtin__.print')
    def test_getSets_whenCountOnly(self, mock_print):
        self.fail('not implemented')

    @mock.patch('__builtin__.print')
    def test_getSets_whenIdOnly(self, mock_print):
        self.fail('not implemented')

    @mock.patch('__builtin__.print')
    @mock.patch('bin.api.execute_api_request')
    def test_getInstructions(self, mock_execute_api_request, mock_print):

        # given
        id = '123'
        directory = None
        set_number = None
        get_sets_response = {'sets': [{'number': '456', 'numberVariant': 1}]}
        get_instructions_response = {
            'status': 'success',
            'matches': 2,
            'instructions': [
                {
                    'URL': 'https://www.lego.com/biassets/bi/6307466.pdf',
                    'description': 'BI 2002/ 2 - 30453 V29'
                },
                {
                    'URL': 'https://www.lego.com/biassets/bi/6307469.pdf',
                    'description': 'BI 2002/ 2 - 30453 V39'
                }
            ]
        }
        mock_execute_api_request.side_effect = [
            get_sets_response,
            get_instructions_response
        ]

        # when
        sets.get_instructions([id], directory, set_number)

        # then
        mock_execute_api_request.assert_has_calls([
            mock.call('getSets', include_hash=True, params={'setID': id}),
            mock.call('getInstructions', setID=id)
        ])
        mock_print.assert_has_calls([
            mock.call('456-1: "BI 2002/ 2 - 30453 V29" https://www.lego.com/biassets/bi/6307466.pdf'),
            mock.call('456-1: "BI 2002/ 2 - 30453 V39" https://www.lego.com/biassets/bi/6307469.pdf'),
        ])

    @mock.patch('__builtin__.print')
    @mock.patch('bin.api.execute_api_request')
    def test_getInstructions_whenNoInstructionsExist(self, mock_execute_api_request, mock_print):

        # given
        id = '123'
        directory = None
        set_number = None
        get_sets_response = {'sets': [{'number': '456', 'numberVariant': 1}]}
        get_instructions_response = {'status': 'success', 'matches': 0, 'instructions': []}
        mock_execute_api_request.side_effect = [
            get_sets_response,
            get_instructions_response
        ]

        # when
        sets.get_instructions([id], directory, set_number)

        # then
        mock_execute_api_request.assert_has_calls([
            mock.call('getSets', include_hash=True, params={'setID': id}),
            mock.call('getInstructions', setID=id)
        ])
        mock_print.assert_called_once_with('No instructions found for 456-1 (123)')

    @mock.patch('bin.api.download_instruction')
    @mock.patch('bin.api.execute_api_request')
    def test_getInstructions_whenDownloading(self, mock_execute_api_request, mock_download_instruction):

        # given
        id = '123'
        directory = '/tmp'
        set_number = None
        get_sets_response = {'sets': [{'number': '456', 'numberVariant': 1}]}
        get_instructions_response = {
            'status': 'success',
            'matches': 2,
            'instructions': [
                {
                    'URL': 'https://www.lego.com/biassets/bi/6307466.pdf',
                    'description': 'BI 2002/ 2 - 30453 V29'
                },
                {
                    'URL': 'https://www.lego.com/biassets/bi/6307469.pdf',
                    'description': 'BI 2002/ 2 - 30453 V39'
                }
            ]
        }
        mock_execute_api_request.side_effect = [
            get_sets_response,
            get_instructions_response
        ]

        # when
        sets.get_instructions([id], directory, set_number)

        # then
        mock_execute_api_request.assert_has_calls([
            mock.call('getSets', include_hash=True, params={'setID': id}),
            mock.call('getInstructions', setID=id)
        ])
        mock_download_instruction.assert_has_calls([
            mock.call(directory, '456-1', get_instructions_response['instructions'][0]),
            mock.call(directory, '456-1', get_instructions_response['instructions'][1])
        ])

    @mock.patch('bin.api.download_instruction')
    @mock.patch('bin.api.execute_api_request')
    def test_getInstructions_whenDownloadingAndSetNumberSupplied(self, mock_execute_api_request, mock_download_instruction):

        # given
        id = '123'
        directory = '/tmp'
        set_number = 'SET_NUM'
        get_instructions_response = {
            'status': 'success',
            'matches': 2,
            'instructions': [
                {
                    'URL': 'https://www.lego.com/biassets/bi/6307466.pdf',
                    'description': 'BI 2002/ 2 - 30453 V29'
                },
                {
                    'URL': 'https://www.lego.com/biassets/bi/6307469.pdf',
                    'description': 'BI 2002/ 2 - 30453 V39'
                }
            ]
        }
        mock_execute_api_request.return_value = get_instructions_response

        # when
        sets.get_instructions([id], directory, set_number)

        # then
        mock_execute_api_request.assert_called_once_with('getInstructions', setID=id)
        mock_download_instruction.assert_has_calls([
            mock.call(directory, set_number, get_instructions_response['instructions'][0]),
            mock.call(directory, set_number, get_instructions_response['instructions'][1])
        ])

    @mock.patch('__builtin__.open')
    @mock.patch('__builtin__.print')
    @mock.patch('bin.api.execute_api_request')
    def test_getInstructions_whenDownloadingAndNoInstructionsExist(self, mock_execute_api_request, mock_print, mock_open):

        # given
        id = '123'
        directory = '/tmp'
        set_number = None
        get_sets_response = {'sets': [{'number': '456', 'numberVariant': 1}]}
        get_instructions_response = {'status': 'success', 'matches': 0, 'instructions': []}
        mock_execute_api_request.side_effect = [
            get_sets_response,
            get_instructions_response
        ]

        # when
        sets.get_instructions([id], directory, set_number)

        # then
        mock_execute_api_request.assert_has_calls([
            mock.call('getSets', include_hash=True, params={'setID': id}),
            mock.call('getInstructions', setID=id)
        ])
        mock_print.assert_called_once_with('No instructions found for 456-1 (123)')
        mock_open.assert_called_once_with('/tmp/456-1_noinstructions.txt', 'wb')


    @mock.patch('__builtin__.print')
    @mock.patch('bin.api.execute_api_request')
    def test_getThemes(self, mock_execute_api_request, mock_print):

        # given
        theme = None
        mock_execute_api_request.return_value = {
            'status': 'success',
            'matches': 2,
            'themes': [
                {
                    'theme': '4 Juniors',
                    'setCount': 24,
                    'subthemeCount': 5,
                    'yearFrom': 2003,
                    'yearTo': 2004
                },
                {
                    'theme': 'Action Wheelers',
                    'setCount': 9,
                    'subthemeCount': 0,
                    'yearFrom': 2000,
                    'yearTo': 2001
                }
            ]
        }

        # when
        sets.get_themes(theme)

        # then
        mock_execute_api_request.assert_called_once_with('getThemes')
        mock_print.assert_has_calls([
            mock.call('4 Juniors (2003-2004): 24 set(s), 5 subtheme(s)'),
            mock.call('Action Wheelers (2000-2001): 9 set(s), 0 subtheme(s)')
        ])

    @mock.patch('__builtin__.print')
    @mock.patch('bin.api.execute_api_request')
    def test_getThemes_withThemeFilter(self, mock_execute_api_request, mock_print):

        # given
        theme = 'Wheelers'
        mock_execute_api_request.return_value = {
            'status': 'success',
            'matches': 2,
            'themes': [
                {
                    'theme': '4 Juniors',
                    'setCount': 24,
                    'subthemeCount': 5,
                    'yearFrom': 2003,
                    'yearTo': 2004
                },
                {
                    'theme': 'Action Wheelers',
                    'setCount': 9,
                    'subthemeCount': 0,
                    'yearFrom': 2000,
                    'yearTo': 2001
                }
            ]
        }

        # when
        sets.get_themes(theme)

        # then
        mock_execute_api_request.assert_called_once_with('getThemes')
        mock_print.assert_has_calls([
            mock.call('Action Wheelers (2000-2001): 9 set(s), 0 subtheme(s)')
        ])

    @mock.patch('__builtin__.print')
    @mock.patch('bin.api.execute_api_request')
    def test_getSubthemes(self, mock_execute_api_request, mock_print):

        # given
        theme = 'Star Wars'
        subtheme = None
        mock_execute_api_request.return_value = {
            'status': 'success',
            'matches': 2,
            'subthemes': [
                {
                    'theme': 'Star Wars',
                    'subtheme': '{None}',
                    'setCount': 3,
                    'yearFrom': 2019,
                    'yearTo': 2019
                },
                {
                    'theme': 'Star Wars',
                    'subtheme': '4 Plus',
                    'setCount': 4,
                    'yearFrom': 2019,
                    'yearTo': 2020
                }
            ]
        }

        # when
        sets.get_subthemes(theme, subtheme)

        # then
        mock_execute_api_request.assert_called_once_with('getSubthemes', Theme=theme)
        mock_print.assert_has_calls([
            mock.call('{None} (2019-2019): 3 set(s)'),
            mock.call('4 Plus (2019-2020): 4 set(s)'),
        ])

    @mock.patch('__builtin__.print')
    @mock.patch('bin.api.execute_api_request')
    def test_getSubthemes_withSubthemeFilter(self, mock_execute_api_request, mock_print):

        # given
        theme = 'Star Wars'
        subtheme = None
        mock_execute_api_request.return_value = {
            'status': 'success',
            'matches': 2,
            'subthemes': [
                {
                    'theme': 'Star Wars',
                    'subtheme': '{None}',
                    'setCount': 3,
                    'yearFrom': 2019,
                    'yearTo': 2019
                },
                {
                    'theme': 'Star Wars',
                    'subtheme': '4 Plus',
                    'setCount': 4,
                    'yearFrom': 2019,
                    'yearTo': 2020
                }
            ]
        }

        # when
        sets.get_subthemes(theme, subtheme)

        # then
        mock_execute_api_request.assert_called_once_with('getSubthemes', Theme=theme)
        mock_print.assert_has_calls([
            mock.call('{None} (2019-2019): 3 set(s)'),
            mock.call('4 Plus (2019-2020): 4 set(s)'),
        ])

    @mock.patch('__builtin__.print')
    @mock.patch('bin.api.execute_api_request')
    def test_getYears(self, mock_execute_api_request, mock_print):

        # given
        theme = 'City'
        mock_execute_api_request.return_value = {
            'status': 'success',
            'matches': 16,
            'years': [
                {
                    'theme': 'City',
                    'year': '2005',
                    'setCount': 46
                },
                {
                    'theme': 'City',
                    'year': '2006',
                    'setCount': 34
                }
            ]
        }

        # when
        sets.get_years(theme)

        # then
        mock_execute_api_request.assert_called_once_with('getYears', Theme=theme)
        mock_print.assert_has_calls([
            mock.call('2005: 46'),
            mock.call('2006: 34')
        ])

    def test__isIso8601Date_whenValid(self):
        # expect
        self.assertTrue(sets._is_iso8601_date('2020-05-05'))

    @mock.patch('sys.exit')
    def test__isIso8601Date_whenInvalid(self, mock_exit):

        # when
        sets._is_iso8601_date('May 5, 2020')

        # then
        mock_exit.assert_called_once_with('ERROR: updated_since must have format yyyy-MM-dd')

    @mock.patch('__builtin__.print')
    def test__printSet(self, mock_print):

        # given
        lego_set = {
            'number': '123',
            'numberVariant': '4',
            'setID': '789',
            'name': 'Set A'
        }

        # when
        sets._print_set(lego_set, False)

        # then
        mock_print.assert_called_once_with('123-4 789 Set A')

    @mock.patch('__builtin__.print')
    def test__printSet_idOnly(self, mock_print):
        # given
        lego_set = {
            'setID': '789'
        }

        # when
        sets._print_set(lego_set, True)

        # then
        mock_print.assert_called_once_with('789')

    def test__isValidOrderBy_whenValid(self):
        # expect
        self.assertTrue(sets._is_valid_order_by('YearFromDESC'))
        self.assertTrue(sets._is_valid_order_by('yearfromdesc'))

    @mock.patch('sys.exit')
    def test__isValidOrderBy_whenInvalid(self, mock_exit):

        # when
        sets._is_valid_order_by('ThemeDESC')

        # then
        mock_exit.assert_called_once_with('ERROR: invalid sort option')

    @mock.patch('bin.api.execute_api_request')
    def test__getSetNumber(self, mock_execute_api_request):

        # given
        set_id = '1394'
        mock_execute_api_request.return_value = {
            "status": "success",
            "matches": 1,
            "sets": [
                {
                    "setID": 1394,
                    "number": "3219",
                    "numberVariant": 1,
                }
            ]
        }

        # when
        set_number = sets._get_set_number(set_id)

        # then
        mock_execute_api_request.assert_called_once_with('getSets', include_hash=True, params={'setID': set_id})

        self.assertEqual('3219-1', set_number)

    @mock.patch('__builtin__.print')
    def test__printInstruction(self, mock_print):

        # given
        set_number = '123-4'
        instruction = {'URL': 'lego.com/123-4.pdf', 'description': '123-4 instructions'}

        # when
        sets._print_instruction(set_number, instruction)

        # then
        mock_print.assert_called_once_with('123-4: "123-4 instructions" lego.com/123-4.pdf')
