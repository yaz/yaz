import inspect
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

    @staticmethod
    def __new__(cls):
        signature = inspect.signature(cls.__init__)

        # set default parameters for Plugin classes
        kwargs = {}
        for parameter in signature.parameters.values():
            if parameter.default is parameter.empty and\
               parameter.kind is parameter.POSITIONAL_OR_KEYWORD and\
               issubclass(parameter.annotation, Plugin):
                kwargs[parameter.name] = parameter.annotation()

        if kwargs:
            init = cls.__init__
            cls.__init__ = lambda self: init(self, **kwargs)

        return super().__new__(cls)
