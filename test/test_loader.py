import unittest

from ..yaz.loader import load

class TestLoader(unittest.TestCase):
    def test_loader(self):
        module = load("./test", "loader")
        self.assertEqual("Done", module.loader_completed)

