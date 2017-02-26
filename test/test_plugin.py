import unittest
import yaz

from test.extension.dependencyinjection import Food, MoreFood
from test.extension.pluginordinal import base as Orginal


class TestPlugin(unittest.TestCase):
    def test_010_dependency_injection(self):
        """Should call dependency setter"""
        food = yaz.get_plugin_instance(Food)
        self.assertEqual("Breakfast is ready", food.breakfast())
        self.assertEqual("BREAKFAST IS READY", food.breakfast(shout=True))

    def test_020_singleton_dependency_injection(self):
        """Should inject the same dependency for different dependent plugins"""
        food = yaz.get_plugin_instance(Food)
        more_food = yaz.get_plugin_instance(MoreFood)
        self.assertEqual(food.get_helper(), more_food.get_helper())

    def test_030_plugin_creation_ordinal(self):
        """Should follow the ordinal when creating the plugin type"""
        ordinal = yaz.get_plugin_instance(Orginal)
        self.assertEqual(["low (8)", "custom (128)", "default (256)", "base (512)", "high (1024)"], ordinal.stack())
