import subprocess
import sys
import unittest

class TestIssue027(unittest.TestCase):
    def test_all_modules_importable(self):
        result = subprocess.run(
            [sys.executable, '-c',
             'import brickset.cache, brickset.sets, brickset.instructions, brickset.minifigs'],
            capture_output=True, text=True
        )
        self.assertEqual(0, result.returncode, msg=result.stderr)
