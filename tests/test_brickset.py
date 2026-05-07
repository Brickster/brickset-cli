import os
import subprocess
import unittest

_BIN = os.path.join(os.path.dirname(__file__), '..', 'bin', 'brickset')


class TestBrickset(unittest.TestCase):

    def test_help(self):
        help_output = subprocess.check_output([_BIN, '-h'], text=True)
        self.assertTrue(help_output.startswith('usage: brickset'))

    def test_sets_limit_rejectsNonInteger(self):
        result = subprocess.run([_BIN, 'sets', '--limit', 'foo'], capture_output=True, text=True)
        self.assertEqual(2, result.returncode)
        self.assertIn('invalid int value', result.stderr)

    def test_minifigs_requiresAtLeastOneFilter(self):
        result = subprocess.run([_BIN, 'minifigs'], capture_output=True, text=True)
        self.assertEqual(2, result.returncode)
        self.assertIn('at least one of --owned, --wanted, --query is required', result.stderr)

    def test_collectionSets_requiresAtLeastOneFlag(self):
        result = subprocess.run([_BIN, 'collection', 'sets', '12345'], capture_output=True, text=True)
        self.assertEqual(2, result.returncode)
        self.assertIn('at least one of --owned, --wanted, --not-wanted, --notes, --rating is required', result.stderr)

    def test_collectionMinifigs_requiresAtLeastOneFlag(self):
        result = subprocess.run([_BIN, 'collection', 'minifigs', 'sw0001'], capture_output=True, text=True)
        self.assertEqual(2, result.returncode)
        self.assertIn('at least one of --owned, --wanted, --not-wanted is required', result.stderr)
