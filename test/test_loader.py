import unittest

from ..yaz.loader import load

class TestLoader(unittest.TestCase):
    def test_loader(self):
        """Should load a module from a given directory"""
        module = load("./test", "loader")
        self.assertEqual("Done", module.loader_completed)

