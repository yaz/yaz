import unittest
import yaz

from yaz.test.extension.dependencyinjection import Food, MoreFood
from yaz.test.extension.pluginordinal import base as Orginal
from yaz.test.extension.pluginextension import Earth, earth_base_class, earth_class, earth_base_class_extension, earth_custom_class, earth_class_extension, earth_custom_class_extension


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

    def test_040_plugin_extension(self):
        """Should allow plugins to extend each other"""
        earth = yaz.get_plugin_instance(Earth)
        self.assertIsInstance(earth, earth_base_class)
        self.assertIsInstance(earth, earth_base_class_extension)
        self.assertIsInstance(earth, earth_class)
        self.assertIsInstance(earth, earth_class_extension)
        self.assertIsInstance(earth, earth_custom_class)
        self.assertIsInstance(earth, earth_custom_class_extension)
        self.assertIsInstance(earth, Earth)
        self.assertEqual(["Earth(earth_custom_class)", "Earth(yaz.CustomPlugin)", "Earth(earth_class)", "Earth(yaz.Plugin)", "Earth(earth_base_class)", "Earth(yaz.BasePlugin)"], earth.chain())