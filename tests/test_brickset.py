import os
import subprocess
import unittest

_BIN = os.path.join(os.path.dirname(__file__), '..', 'bin', 'brickset')


class TestBrickset(unittest.TestCase):

  def test_help(self):
    help_output = subprocess.check_output([_BIN, '-h'], text=True)
    self.assertTrue(help_output.startswith('usage: brickset'))
