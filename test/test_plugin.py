import unittest

from ..yaz.plugin import BasePlugin

from test.extension.dependencyinjection import Food, MoreFood
import test.extension.pluginordinal

class TestPlugin(unittest.TestCase):
    def test_depencency_injection(self):
        """Should inject required plugins into constructor"""
        food = Food()
        self.assertEqual("Breakfast is ready", food.breakfast())
        self.assertEqual("BREAKFAST IS READY", food.breakfast(shout=True))

    def testPluginSingleton(self):
        """Should inject the same dependency for different plugins"""
        self.assertEqual(Food().get_helper(), MoreFood().get_helper())

    def testPluginCreationOrdinal(self):
        """Should follow the ordinal when creating the plugin type"""
        plugins = BasePlugin.get_yaz_plugin_list()
        Ordinal = plugins["Ordinal"]
        self.assertEqual(["low (8)", "base (128)", "default (256)", "custom (512)", "high (1024)"], Ordinal().stack())
