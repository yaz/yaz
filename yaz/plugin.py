import inspect
import collections

from .decorator import decorator
from .log import logger

__all__ = ["dependency", "get_plugin_instance", "BasePlugin", "Plugin", "CustomPlugin"]
_yaz_plugin_classes = {}
_yaz_plugin_instance_cache = {}


@decorator
def dependency(func, **config):
    """Declare a setter method to be called just after initializing a yaz.Plugin

    This decorator allows one or more plugin dependencies
    to be injected.  For example:

        class Helper(yaz.Plugin):
            pass

        class HelloWorld(yaz.Plugin):
            def __init__(self):
                self.helper = None

            @yaz.dependency
            def set_helper(self, helper: Helper):
                self.helper = helper

    In the above example, when the HelloWorld plugin is initialized,
    the set_helper method will be called immediately after the constructor
    finishes.

    Multiple dependencies may be injected in a single @yaz.dependency method.
    """
    func.yaz_dependency_config = config
    return func


def get_plugin_list():
    """Finds all yaz plugins and returns them in a __qualname__: plugin_class dictionary"""
    global _yaz_plugin_classes

    def get_recursively(cls, plugin_list):
        for plugin in cls.__subclasses__():
            if not (plugin.yaz_is_final() or plugin.__qualname__ in _yaz_plugin_classes):
                plugin_list[plugin.__qualname__].append(plugin)
            get_recursively(plugin, plugin_list)
        return plugin_list

    def include_class(candidate, classes):
        for cls in classes:
            if candidate is cls:
                continue

            if issubclass(cls, candidate):
                return False

        return True

    def get_plugin_type(qualname, plugins):
        classes = sorted(plugins, key=lambda plugin: plugin.yaz_get_ordinal())

        # exclude classes that are implicitly included as parent classes
        classes = [cls for cls in classes if include_class(cls, classes)]
        logger.debug("New plugin class \"%s\" extending %s", qualname, [cls for cls in classes])

        return type(qualname, tuple(classes) + (Final,), {})

    logger.debug("Plugin list: %s" % _yaz_plugin_classes)

    # find all Plugin classes recursively
    plugin_list = get_recursively(BasePlugin, collections.defaultdict(list))

    # combine all classes into their Plugin class (i.e. multiple inherited plugin)
    _yaz_plugin_classes.update((qualname, get_plugin_type(qualname, plugins))
                               for qualname, plugins
                               in plugin_list.items())

    assert isinstance(_yaz_plugin_classes, dict), type(_yaz_plugin_classes)
    assert all(isinstance(qualname, str) for qualname in _yaz_plugin_classes.keys()), "Every key should be a string"
    assert all(issubclass(plugin_class, Final) for plugin_class in _yaz_plugin_classes.values()), "Every value should be a 'Final' plugin"

    return _yaz_plugin_classes


def get_plugin_instance(plugin_class, *args, **kwargs):
    """Returns an instance of a fully initialized plugin class

    Every plugin class is kept in a plugin cache, effectively making
    every plugin into a singleton object.

    When a plugin has a yaz.dependency decorator, it will be called
    as well, before the instance is returned.
    """
    assert issubclass(plugin_class, BasePlugin), type(plugin_class)

    global _yaz_plugin_instance_cache

    qualname = plugin_class.__qualname__
    if not qualname in _yaz_plugin_instance_cache:
        plugin_class = get_plugin_list()[qualname]
        _yaz_plugin_instance_cache[qualname] = plugin = plugin_class(*args, **kwargs)

        # find any yaz.dependency decorators, and call them when necessary
        funcs = [func
                 for _, func
                 in inspect.getmembers(plugin)
                 if inspect.ismethod(func) and hasattr(func, "yaz_dependency_config")]

        for func in funcs:
            signature = inspect.signature(func)
            assert all(parameter.kind is parameter.POSITIONAL_OR_KEYWORD and issubclass(parameter.annotation, BasePlugin) for parameter in signature.parameters.values()), "All parameters for {} must type hint to a BasePlugin".format(func)
            func(*[get_plugin_instance(parameter.annotation)
                   for parameter
                   in signature.parameters.values()])

    return _yaz_plugin_instance_cache[qualname]


# The Final class is used to mark a plugin class as Final, this
# is necessary to avoid constructing them again when the _yaz_plugin_classes
# variable is cleared in some way
#
# Purposefully *not* specifying a docstring, because it would be used in
# the documentation of the resulting plugin when --help is called on the console
class Final:
    @staticmethod
    def yaz_is_final():
        return True


# The BasePlugin is used to declare a class as a yaz plugin.  The BasePlugin
# has a high ordinal, which has direct effect on the multi-class
# extension used by yaz when constructing the final plugin class.
#
# This class is typically used when defining an importable yaz plugin.
#
# Purposefully *not* specifying a docstring, because it would be used in
# the documentation of the resulting plugin when --help is called on the console
class BasePlugin:
    @staticmethod
    def yaz_is_final():
        return False

    @staticmethod
    def yaz_get_ordinal():
        # typically used from a yaz_foo_plugin
        return 512


# The Plugin is used to declare a class as a yaz plugin.  The Plugin
# has a medium ordinal, which has direct effect on the multi-class
# extension used by yaz when constructing the final plugin class.
#
# This class is used when defining a plugin class that may or may not
# have a matching importable yaz plugin.  When in doubt, use this class!
#
# Purposefully *not* specifying a docstring, because it would be used in
# the documentation of the resulting plugin when --help is called on the console
class Plugin(BasePlugin):
    @staticmethod
    def yaz_get_ordinal():
        # typically used from a project configuration
        return 256


# The Plugin is used to declare a class as a yaz plugin.  The CustomPlugin
# has a low ordinal, which has direct effect on the multi-class
# extension used by yaz when constructing the final plugin class.
#
# This class is used when defining a plugin class that is used
# to override or extend features of existing plugins.  Typically seen in
# ~/.yaz/plugin_extension/ files.
#
# Purposefully *not* specifying a docstring, because it would be used in
# the documentation of the resulting plugin when --help is called on the console
class CustomPlugin(Plugin):
    @staticmethod
    def yaz_get_ordinal():
        # typically used from a custom user configuration
        return 128
