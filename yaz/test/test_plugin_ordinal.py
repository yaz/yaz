#!/usr/bin/env python3

import yaz


class PluginOrdinal(yaz.Plugin):
    @staticmethod
    def yaz_get_ordinal():
        return 8

    @yaz.task
    def stack(self):
        return ["low ({})".format(low.yaz_get_ordinal())] + super().stack()


low = PluginOrdinal


class PluginOrdinal(yaz.Plugin):
    @staticmethod
    def yaz_get_ordinal():
        return 1024

    @yaz.task
    def stack(self):
        return ["high ({})".format(high.yaz_get_ordinal())]


high = PluginOrdinal


class PluginOrdinal(yaz.Plugin):
    @yaz.task
    def stack(self):
        return ["default ({})".format(default.yaz_get_ordinal())] + super().stack()


default = PluginOrdinal


class PluginOrdinal(yaz.BasePlugin):
    @yaz.task
    def stack(self):
        return ["base ({})".format(base.yaz_get_ordinal())] + super().stack()


base = PluginOrdinal


class PluginOrdinal(yaz.CustomPlugin):
    @yaz.task
    def stack(self):
        return ["custom ({})".format(custom.yaz_get_ordinal())] + super().stack()


custom = PluginOrdinal


class Test(yaz.TestCase):
    def test_010(self):
        """Should follow the ordinal when creating the plugin type"""
        ordinal = yaz.get_plugin_instance(PluginOrdinal)
        self.assertEqual(["low (8)", "custom (128)", "default (256)", "base (512)", "high (1024)"], ordinal.stack())


if __name__ == "__main__":
    yaz.main()
