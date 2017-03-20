#!/usr/bin/env python3

import yaz


class Water(yaz.BasePlugin):
    """water-base-plugin"""

    @yaz.task
    def required(self, pos1: str, pos2: str, pos3: str, pos_or_key1: str = "POS_OR_KEY1", pos_or_key2: str = "POS_OR_KEY2", pos_or_key3: str = "POS_OR_KEY3", *, key1: str = "KEY1", key2: str = "KEY2", key3: str = "KEY3"):
        """required from water-base-plugin"""
        return [pos1, pos2, pos3, pos_or_key1, pos_or_key2, pos_or_key3, key1, key2, key3]


water_base_plugin_class = Water


class Water(yaz.Plugin):
    """water-plugin"""

    @yaz.task
    def required(self, pos1: str, pos2: str, pos_or_key1: str = "POS_OR_KEY1", pos_or_key2: str = "alt-POS_OR_KEY2", *args, key1: str = "KEY1", key2: str = "alt-KEY2", extra2: str = "EXTRA2", **kwargs):
        """required from water-base"""
        return super().required(pos1, pos2, pos_or_key1=pos_or_key1, pos_or_key2=pos_or_key2, key1=key1, key2=key2, *args, **kwargs) + [extra2]


water_plugin_class = Water


class Water(yaz.CustomPlugin):
    """water-custom-plugin"""

    @yaz.task
    def required(self, pos1: str, pos_or_key1: str = "alt-POS_OR_KEY1", *args, key1: str = "alt-KEY1", extra1: str = "EXTRA1", **kwargs):
        """required from water-custom-plugin"""
        return super().required(pos1, pos_or_key1=pos_or_key1, key1=key1, *args, **kwargs) + [extra1]


water_custom_plugin_class = Water

if __name__ == "__main__":
    yaz.main()
