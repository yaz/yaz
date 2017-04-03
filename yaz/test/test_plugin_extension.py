#!/usr/bin/env python3

"""

Below we define several plugins with the name 'Earth'.
Some of these classes extend from each other, and hence
obtain the yaz ordinal defined in the base class.

The expected method resolution is as follows:

1. earth_custom_class_extension (ordinal indirectly from yaz.CustomPlugin)
1. earth_custom_class (ordinal from yaz.CustomPlugin)
2. earth_plugin_class_extension (ordinal indirectly from yaz.Plugin)
3. earth_plugin_class (ordinal from yaz.Plugin)
4. earth_base_class_extension (ordinal indirectly from yaz.BasePlugin)
5. earth_base_class (ordinal from yaz.BasePlugin)
"""

import yaz


class PluginExtensionEarth(yaz.BasePlugin):
    @yaz.task
    def chain(self):
        return ["Earth(yaz.BasePlugin)"]


earth_base_class = PluginExtensionEarth


class PluginExtensionEarth(yaz.Plugin):
    @yaz.task
    def chain(self):
        return ["Earth(yaz.Plugin)"] + super().chain()


earth_class = PluginExtensionEarth


class PluginExtensionEarth(yaz.CustomPlugin):
    @yaz.task
    def chain(self):
        return ["Earth(yaz.CustomPlugin)"] + super().chain()


earth_custom_class = PluginExtensionEarth


class PluginExtensionEarth(earth_base_class):
    @yaz.task
    def chain(self):
        return ["Earth(earth_base_class)"] + super().chain()


earth_base_class_extension = PluginExtensionEarth


class PluginExtensionEarth(earth_class):
    @yaz.task
    def chain(self):
        return ["Earth(earth_class)"] + super().chain()


earth_class_extension = PluginExtensionEarth


class PluginExtensionEarth(earth_custom_class):
    @yaz.task
    def chain(self):
        return ["Earth(earth_custom_class)"] + super().chain()


earth_custom_class_extension = PluginExtensionEarth


class Test(yaz.TestCase):
    def test_040_plugin_extension(self):
        """Should allow plugins to extend each other"""
        earth = yaz.get_plugin_instance(PluginExtensionEarth)
        self.assertIsInstance(earth, earth_base_class)
        self.assertIsInstance(earth, earth_base_class_extension)
        self.assertIsInstance(earth, earth_class)
        self.assertIsInstance(earth, earth_class_extension)
        self.assertIsInstance(earth, earth_custom_class)
        self.assertIsInstance(earth, earth_custom_class_extension)
        self.assertIsInstance(earth, PluginExtensionEarth)
        self.assertEqual(["Earth(earth_custom_class)", "Earth(yaz.CustomPlugin)", "Earth(earth_class)", "Earth(yaz.Plugin)", "Earth(earth_base_class)", "Earth(yaz.BasePlugin)"], earth.chain())


if __name__ == "__main__":
    yaz.main()
