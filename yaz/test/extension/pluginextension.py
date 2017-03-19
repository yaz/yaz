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


class Earth(yaz.BasePlugin):
    @yaz.task
    def chain(self):
        return ["Earth(yaz.BasePlugin)"]


earth_base_class = Earth


class Earth(yaz.Plugin):
    @yaz.task
    def chain(self):
        return ["Earth(yaz.Plugin)"] + super().chain()


earth_class = Earth


class Earth(yaz.CustomPlugin):
    @yaz.task
    def chain(self):
        return ["Earth(yaz.CustomPlugin)"] + super().chain()


earth_custom_class = Earth


class Earth(earth_base_class):
    @yaz.task
    def chain(self):
        return ["Earth(earth_base_class)"] + super().chain()


earth_base_class_extension = Earth


class Earth(earth_class):
    @yaz.task
    def chain(self):
        return ["Earth(earth_class)"] + super().chain()


earth_class_extension = Earth


class Earth(earth_custom_class):
    @yaz.task
    def chain(self):
        return ["Earth(earth_custom_class)"] + super().chain()


earth_custom_class_extension = Earth

if __name__ == "__main__":
    yaz.main()
