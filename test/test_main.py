import sys
import unittest

from yaz import main


class TestMain(unittest.TestCase):
    def test_main(self):
        """Should load a module from a given directory"""
        result = main([sys.argv[0], "--message", "Echo!"], ["say"])
        self.assertEqual("Echo!", result)

    def test_main_runs_help(self):
        """Should print help when not given arguments"""
        # todo: check stdout
        main([sys.argv[0]])