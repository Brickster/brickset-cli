import unittest
from unittest import mock

from brickset import cache
from brickset import sets


class TestSets(unittest.TestCase):

    @mock.patch('brickset.cache.update_cache')
    @mock.patch('builtins.print')
    @mock.patch('brickset.api.execute_api_request')
    def test_getSets(self, mock_api, mock_print, mock_update_cache):
        mock_api.return_value = {'sets': [], 'matches': 0}
        sets.get_sets(
            sets.SetFilters(query='star wars'),
            limit=20, order_by=None, extended=False, id_only=False, count=False
        )
        mock_api.assert_called_once_with('getSets', include_hash=True, params={'query': 'star wars', 'pageSize': 20})

    def test_getSets_whenUpdatedSinceIsInvalid(self):
        with self.assertRaises(SystemExit) as cm:
            sets.get_sets(
                sets.SetFilters(updated_since='not-a-date'),
                limit=20, order_by=None, extended=False, id_only=False, count=False
            )
        self.assertEqual('ERROR: updated_since must have format yyyy-MM-dd', cm.exception.code)

    def test_getSets_whenOrderByIsInvalid(self):
        with self.assertRaises(SystemExit) as cm:
            sets.get_sets(
                sets.SetFilters(),
                limit=20, order_by='Invalid', extended=False, id_only=False, count=False
            )
        self.assertEqual('ERROR: invalid sort option', cm.exception.code)

    def test_getSets_whenLimitIsInvalid(self):
        with self.assertRaises(SystemExit) as cm:
            sets.get_sets(
                sets.SetFilters(),
                limit=501, order_by=None, extended=False, id_only=False, count=False
            )
        self.assertEqual('ERROR: limit must be between 1 and 500', cm.exception.code)

    @mock.patch('brickset.cache.update_cache')
    @mock.patch('builtins.print')
    @mock.patch('brickset.api.execute_api_request')
    def test_getSets_whenCountOnly(self, mock_api, mock_print, mock_update_cache):
        mock_api.return_value = {'sets': [], 'matches': 42}
        sets.get_sets(
            sets.SetFilters(query='star wars'),
            limit=20, order_by=None, extended=False, id_only=False, count=True
        )
        mock_api.assert_called_once_with('getSets', include_hash=True, params={'query': 'star wars', 'pageSize': 0})
        mock_print.assert_called_once_with(42)

    @mock.patch('brickset.cache.update_cache')
    @mock.patch('builtins.print')
    @mock.patch('brickset.api.execute_api_request')
    def test_getSets_whenIdOnly(self, mock_api, mock_print, mock_update_cache):
        mock_api.return_value = {'sets': [{'setID': '789'}], 'matches': 1}
        sets.get_sets(
            sets.SetFilters(query='star wars'),
            limit=20, order_by=None, extended=False, id_only=True, count=False
        )
        mock_print.assert_called_once_with('789')

    @mock.patch('brickset.cache.update_cache', return_value={'sets': {'1394': '3219-1', '3219-1': '1394'}})
    @mock.patch('brickset.cache.get_cache', return_value={'sets': {}})
    @mock.patch('brickset.api.execute_api_request')
    def test__getSetNumber(self, mock_api, mock_get_cache, mock_update_cache):
        mock_api.return_value = {
            'status': 'success',
            'matches': 1,
            'sets': [{'setID': 1394, 'number': '3219', 'numberVariant': 1}]
        }

        set_number = cache._get_set_number('1394')

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

    def test_buildFilterParams_allFields(self):
        filters = sets.SetFilters(
            id='123',
            set_number=['456-1', '789-1'],
            theme=['Star Wars', 'City'],
            subtheme=['Clone Wars'],
            year=['2020', '2021'],
            tag='exclusive',
            owned=True,
            wanted=True,
        )
        self.assertEqual({
            'setID': '123',
            'setNumber': '456-1,789-1',
            'theme': 'Star Wars,City',
            'subtheme': 'Clone Wars',
            'year': '2020,2021',
            'tag': 'exclusive',
            'owned': 1,
            'wanted': 1,
        }, sets._build_filter_params(filters))

    @mock.patch('brickset.cache.update_cache')
    @mock.patch('builtins.print')
    @mock.patch('brickset.api.execute_api_request')
    def test_getSets_withUpdatedSince(self, mock_api, mock_print, mock_update_cache):
        mock_api.return_value = {'sets': [], 'matches': 0}
        sets.get_sets(
            sets.SetFilters(updated_since='2024-01-01'),
            limit=20, order_by=None, extended=False, id_only=False, count=False
        )
        mock_api.assert_called_once_with('getSets', include_hash=True, params={
            'updatedSince': '2024-01-01', 'pageSize': 20
        })

    @mock.patch('brickset.cache.update_cache')
    @mock.patch('builtins.print')
    @mock.patch('brickset.api.execute_api_request')
    def test_getSets_withOrderBy(self, mock_api, mock_print, mock_update_cache):
        mock_api.return_value = {'sets': [], 'matches': 0}
        sets.get_sets(
            sets.SetFilters(),
            limit=20, order_by='YearFrom', extended=False, id_only=False, count=False
        )
        mock_api.assert_called_once_with('getSets', include_hash=True, params={
            'orderBy': 'YearFrom', 'pageSize': 20
        })

    @mock.patch('brickset.cache.update_cache')
    @mock.patch('builtins.print')
    @mock.patch('brickset.api.execute_api_request')
    def test_getSets_whenExtended(self, mock_api, mock_print, mock_update_cache):
        mock_api.return_value = {'sets': [], 'matches': 0}
        sets.get_sets(
            sets.SetFilters(),
            limit=20, order_by=None, extended=True, id_only=False, count=False
        )
        mock_api.assert_called_once_with('getSets', include_hash=True, params={
            'extendedData': 1, 'pageSize': 20
        })

    @mock.patch('brickset.sets._is_valid_limit', return_value=False)
    def test_getSets_whenLimitValidationReturnsFalse(self, _mock):
        self.assertIsNone(sets.get_sets(
            sets.SetFilters(), limit=20, order_by=None, extended=False, id_only=False, count=False
        ))

    @mock.patch('brickset.api.execute_api_request')
    def test_updateSet_whenOwned1(self, mock_api):
        sets.update_set('123', owned=1, wanted=None, notes=None, rating=None)
        mock_api.assert_called_once_with('setCollection', include_hash=True, setID='123', params={'own': 1})

    @mock.patch('brickset.api.execute_api_request')
    def test_updateSet_whenQtyOwned(self, mock_api):
        sets.update_set('123', owned=5, wanted=None, notes=None, rating=None)
        mock_api.assert_called_once_with('setCollection', include_hash=True, setID='123', params={'qtyOwned': 5})

    @mock.patch('brickset.api.execute_api_request')
    def test_updateSet_whenWanted(self, mock_api):
        sets.update_set('123', owned=None, wanted=True, notes=None, rating=None)
        mock_api.assert_called_once_with('setCollection', include_hash=True, setID='123', params={'want': 1})

    @mock.patch('brickset.api.execute_api_request')
    def test_updateSet_whenNotWanted(self, mock_api):
        sets.update_set('123', owned=None, wanted=False, notes=None, rating=None)
        mock_api.assert_called_once_with('setCollection', include_hash=True, setID='123', params={'want': 0})

    @mock.patch('brickset.api.execute_api_request')
    def test_updateSet_withNotesAndRating(self, mock_api):
        sets.update_set('123', owned=None, wanted=None, notes='Great set', rating=5)
        mock_api.assert_called_once_with('setCollection', include_hash=True, setID='123', params={
            'notes': 'Great set', 'rating': 5
        })

    @mock.patch('builtins.print')
    def test__printSet_whenOwned(self, mock_print):
        lego_set = {
            'number': '123', 'numberVariant': '4', 'setID': '789', 'name': 'Set A',
            'collection': {'owned': True, 'qtyOwned': 2, 'wanted': False}
        }
        sets._print_set(lego_set, False)
        mock_print.assert_called_once_with('123-4 789 Set A (2 owned)')

    @mock.patch('builtins.print')
    def test__printSet_whenWanted(self, mock_print):
        lego_set = {
            'number': '123', 'numberVariant': '4', 'setID': '789', 'name': 'Set A',
            'collection': {'owned': False, 'wanted': True}
        }
        sets._print_set(lego_set, False)
        mock_print.assert_called_once_with('123-4 789 Set A (wanted)')
