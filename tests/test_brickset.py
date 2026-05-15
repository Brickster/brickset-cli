import os
import subprocess
import unittest

_BIN = os.path.join(os.path.dirname(__file__), '..', 'bin', 'brickset')


class TestBrickset(unittest.TestCase):

    def test_help(self):
        help_output = subprocess.check_output([_BIN, '-h'], text=True)
        self.assertTrue(help_output.startswith('usage: brickset'))

    def test_sets_requiresAtLeastOneFilter(self):
        result = subprocess.run([_BIN, 'sets'], capture_output=True, text=True)
        self.assertEqual(2, result.returncode)
        self.assertIn('at least one filter is required', result.stderr)

    def test_sets_limit_rejectsNonInteger(self):
        result = subprocess.run([_BIN, 'sets', '--limit', 'foo'], capture_output=True, text=True)
        self.assertEqual(2, result.returncode)
        self.assertIn('invalid int value', result.stderr)

    def test_minifigs_requiresAtLeastOneFilter(self):
        result = subprocess.run([_BIN, 'minifigs'], capture_output=True, text=True)
        self.assertEqual(2, result.returncode)
        self.assertIn('at least one of --owned, --wanted, --query is required', result.stderr)

    def test_collectionSets_rating_rejectsOutOfRange(self):
        result = subprocess.run([_BIN, 'collection', 'sets', '12345', '--rating', '6'], capture_output=True, text=True)
        self.assertEqual(2, result.returncode)
        self.assertIn('invalid choice: 6', result.stderr)

    def test_collectionSets_rating_rejectsNegative(self):
        result = subprocess.run([_BIN, 'collection', 'sets', '12345', '--rating', '-1'], capture_output=True, text=True)
        self.assertEqual(2, result.returncode)

    def test_collectionSets_rating_rejectsNonInteger(self):
        result = subprocess.run([_BIN, 'collection', 'sets', '12345', '--rating', 'foo'], capture_output=True, text=True)
        self.assertEqual(2, result.returncode)
        self.assertIn('invalid int value', result.stderr)

    def test_collectionSets_requiresAtLeastOneFlag(self):
        result = subprocess.run([_BIN, 'collection', 'sets', '12345'], capture_output=True, text=True)
        self.assertEqual(2, result.returncode)
        self.assertIn('at least one of --owned, --wanted, --not-wanted, --notes, --rating is required', result.stderr)

    def test_collectionMinifigs_requiresAtLeastOneFlag(self):
        result = subprocess.run([_BIN, 'collection', 'minifigs', 'sw0001'], capture_output=True, text=True)
        self.assertEqual(2, result.returncode)
        self.assertIn('at least one of --owned, --wanted, --not-wanted is required', result.stderr)

    def test_sets_positional_setNumber_isAccepted(self):
        result = subprocess.run([_BIN, 'sets', '50505-1'], capture_output=True, text=True)
        self.assertNotEqual(2, result.returncode)

    def test_sets_positional_setId_isAccepted(self):
        result = subprocess.run([_BIN, 'sets', '1234'], capture_output=True, text=True)
        self.assertNotEqual(2, result.returncode)

    def test_sets_positional_cannotCombineWithSetId(self):
        result = subprocess.run([_BIN, 'sets', '1234', '--set-id', '5678'], capture_output=True, text=True)
        self.assertEqual(2, result.returncode)
        self.assertIn('cannot be combined', result.stderr)

    def test_sets_positional_cannotCombineWithSetNumber(self):
        result = subprocess.run([_BIN, 'sets', '50505-1', '--set-number', '60001-1'], capture_output=True, text=True)
        self.assertEqual(2, result.returncode)
        self.assertIn('cannot be combined', result.stderr)

    def test_instructions_positional_mixedTypesError(self):
        result = subprocess.run([_BIN, 'instructions', '50505-1', '1234'], capture_output=True, text=True)
        self.assertEqual(2, result.returncode)
        self.assertIn('must all be set IDs or all set numbers', result.stderr)

    def test_collectionSets_positional_setNumber_isAccepted(self):
        # Exit 2 is expected (no config → lookup returns nothing), but the error must come
        # from our dispatch ("no set found"), not from argparse rejecting the argument.
        result = subprocess.run([_BIN, 'collection', 'sets', '50505-1', '--owned'], capture_output=True, text=True)
        self.assertIn('no set found for set number', result.stderr)

    def test_collectionSets_positional_cannotCombineWithSetId(self):
        result = subprocess.run(
            [_BIN, 'collection', 'sets', '1234', '--set-id', '5678', '--owned'],
            capture_output=True, text=True
        )
        self.assertEqual(2, result.returncode)
        self.assertIn('cannot be combined', result.stderr)

    def test_collectionSets_positional_cannotCombineWithSetNumber(self):
        result = subprocess.run(
            [_BIN, 'collection', 'sets', '50505-1', '--set-number', '60001-1', '--owned'],
            capture_output=True, text=True
        )
        self.assertEqual(2, result.returncode)
        self.assertIn('cannot be combined', result.stderr)

    def test_collectionSets_requiresIdentifier(self):
        result = subprocess.run([_BIN, 'collection', 'sets', '--owned'], capture_output=True, text=True)
        self.assertEqual(2, result.returncode)
        self.assertIn('an identifier is required', result.stderr)
