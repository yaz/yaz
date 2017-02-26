import inspect
import collections

from .decorator import decorator

__all__ = ["dependency", "get_plugin_instance", "BasePlugin", "Plugin", "CustomPlugin"]

_yaz_plugin_classes = None
_yaz_plugin_instance_cache = {}


@decorator
def dependency(func, **config):
    func.yaz_dependency_config = config
    return func


def get_plugin_list():
    global _yaz_plugin_classes

    if _yaz_plugin_classes is None:
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
        plugin_list = get_recursively(BasePlugin, collections.defaultdict(list))

        # combine all classes into their Plugin class (i.e. multiple inherited plugin)
        _yaz_plugin_classes = dict((qualname, get_plugin_type(qualname, plugins))
                                   for qualname, plugins
                                   in plugin_list.items())

    return _yaz_plugin_classes


def get_plugin_class(plugin_class):
    assert issubclass(plugin_class, BasePlugin), type(plugin_class)

    global _yaz_plugin_classes
    classes = get_plugin_list()
    return classes.get(plugin_class.__qualname__)


def get_plugin_instance(plugin_class, *args, **kwargs):
    assert issubclass(plugin_class, BasePlugin), type(plugin_class)

    global _yaz_plugin_instance_cache
    if not plugin_class.__qualname__ in _yaz_plugin_instance_cache:
        plugin_class = get_plugin_class(plugin_class)
        _yaz_plugin_instance_cache[plugin_class.__qualname__] = plugin = plugin_class(*args, **kwargs)

        funcs = [func
                 for _, func
                 in inspect.getmembers(plugin)
                 if inspect.ismethod(func) and hasattr(func, "yaz_dependency_config")]

        for func in funcs:
            signature = inspect.signature(func)
            assert all(parameter.kind is parameter.POSITIONAL_OR_KEYWORD and issubclass(parameter.annotation, BasePlugin) for parameter in signature.parameters.values()), "All parameters for {} must type hint to BasePlugin".format(func)
            func(*[get_plugin_instance(parameter.annotation)
                   for parameter
                   in signature.parameters.values()])

    return _yaz_plugin_instance_cache[plugin_class.__qualname__]


class Final:
    @staticmethod
    def yaz_is_final():
        return True


class BasePlugin:
    @staticmethod
    def yaz_is_final():
        return False

    @staticmethod
    def yaz_get_ordinal():
        # typically used from a yaz_foo_plugin
        return 512


class Plugin(BasePlugin):
    @staticmethod
    def yaz_get_ordinal():
        # typically used from a project configuration
        return 256


class CustomPlugin(Plugin):
    @staticmethod
    def yaz_get_ordinal():
        # typically used from a custom user configuration
        return 128
