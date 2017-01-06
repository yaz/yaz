import unittest

from ..yaz.plugin import Plugin

from test.dependencyinjection import Food, MoreFood
import test.pluginordinal

class TestPlugin(unittest.TestCase):
    def testDepencencyInjection(self):
        """Should inject required plugins into constructor"""
        food = Food()
        assert food.breakfast() == "Breakfast is ready"
        assert food.breakfast(shout=True) == "BREAKFAST IS READY"

    def testPluginSingleton(self):
        """Should inject the same dependency for different plugins"""
        assert Food().get_helper() is MoreFood().get_helper()

    def testPluginCreationOrdinal(self):
        """Should follow the ordinal when creating the plugin type"""
        plugins = Plugin.get_yaz_plugin_list()
        Ordinal = plugins["Ordinal"]
        assert Ordinal().stack() == ["low (8)", "default (128)", "high (1024)"]
