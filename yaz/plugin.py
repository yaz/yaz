import inspect
import collections


class Final:
    @staticmethod
    def yaz_is_final():
        return True


class BasePlugin:
    _yaz_plugin_cache = {}

    @staticmethod
    def yaz_is_final():
        return False

    @staticmethod
    def yaz_get_ordinal():
        # typically used from a yaz_foo_plugin
        return 128

    @classmethod
    def get_yaz_plugin_list(cls):
        def get_recursively(cls, plugin_list):
            for plugin in cls.__subclasses__():
                if not plugin.yaz_is_final():
                    plugin_list[plugin.__qualname__].append(plugin)
                get_recursively(plugin, plugin_list)
            return plugin_list

        def get_plugin_type(qualname, plugins):
            classes = sorted(plugins, key=lambda plugin: plugin.yaz_get_ordinal())
            return type(qualname, (Final,) + tuple(classes), {})

        # find all Plugin classes recursively
        plugin_list = get_recursively(cls, collections.defaultdict(list))

        # combine all classes into their Plugin class (i.e. multiple inherited plugin)
        return dict((qualname, get_plugin_type(qualname, plugins))
                    for qualname, plugins
                    in plugin_list.items())

    @staticmethod
    def __new__(cls, *args):
        signature = inspect.signature(cls.__init__)

        # initialize plugin dependencies
        kwargs = {}
        for parameter in signature.parameters.values():
            if parameter.default is parameter.empty \
                    and parameter.kind is parameter.POSITIONAL_OR_KEYWORD \
                    and issubclass(parameter.annotation, Plugin):
                if parameter.annotation not in cls._yaz_plugin_cache:
                    cls._yaz_plugin_cache[parameter.annotation] = parameter.annotation()
                kwargs[parameter.name] = cls._yaz_plugin_cache[parameter.annotation]

        if kwargs:
            init = cls.__init__
            cls.__init__ = lambda self: init(self, **kwargs)

        return super().__new__(cls)


class Plugin(BasePlugin):
    @staticmethod
    def yaz_get_ordinal():
        # typically used from a project configuration
        return 256


class CustomPlugin(Plugin):
    @staticmethod
    def yaz_get_ordinal():
        # typically used from a custom user configuration
        return 512
