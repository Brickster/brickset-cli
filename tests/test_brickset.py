import subprocess
import unittest


class TestBrickset(unittest.TestCase):

  def test_help(self):
    # when
    abandon_output = subprocess.check_output('../bin/brickset -h'.split())

    # then
    self.assertTrue(abandon_output.startswith('usage: brickset'))
