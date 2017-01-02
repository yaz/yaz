import collections
import re

class Plugin:
    @classmethod
    def get_yaz_plugin_ordinal(cls, default=128):
        patterns = [
            (512, '^yaz[.]plugins[.]'),
            (256, '^__main__[.]'),
        ]
        for ordinal, pattern in patterns:
            if re.match(pattern, "{cls.__module__}.{cls.__qualname__}".format(cls=cls)):
                return ordinal
        return default

    @classmethod
    def get_yaz_plugin_list(cls):
        # find all Plugin classes
        plugin_list = collections.defaultdict(list)
        for plugin in cls.__subclasses__():
            plugin_list[plugin.__qualname__].append(plugin)

        # combine all classes into their Plugin class (i.e. multiple inherited plugin)
        return dict((qualname, type(qualname, tuple(sorted(plugins, key=lambda plugin: plugin.get_yaz_plugin_ordinal())), {}))
                    for qualname, plugins
                    in plugin_list.items())
