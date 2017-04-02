import asyncio
import datetime
import inspect
import re

from .decorator import decorator
from .log import logger
from .plugin import BasePlugin, get_plugin_instance, get_plugin_list

__all__ = ["task", "get_task_tree"]
_task_list = {}


class Task:
    """The Task class is created for every @yaz.task found"""

    class Documentation:
        def __init__(self, full):
            if full:
                match = re.match(r"^(?P<first_line>.+)\n\n(?P<everything_else>.+)$", full, re.MULTILINE)
                if match:
                    short = match.group("first_line")
                    long = match.group("everything_else")
                else:
                    short = full
                    long = ""
            else:
                full = ""
                short = ""
                long = ""

            self.full = full.strip()
            self.short = short.strip()
            self.long = long.strip()

    def __init__(self, plugin_class, func, config):
        assert plugin_class is None or issubclass(plugin_class, BasePlugin)
        assert callable(func)
        assert isinstance(config, dict)
        self.plugin_class = plugin_class
        self.func = func
        self.config = config

    @property
    def plugin_documentation(self):
        """Returns documentation for the plugin class"""
        return self.Documentation(inspect.getdoc(self.plugin_class))

    @property
    def documentation(self):
        """Returns documentation for the task function"""
        return self.Documentation(inspect.getdoc(self.func))

    @property
    def qualified_name(self):
        """Returns the __qualname__ of this Task"""
        return self.func.__qualname__

    def __call__(self, **kwargs):
        """Prepare dependencies and call this Task"""
        start = datetime.datetime.now()
        logger.info("Start task %s", self)
        try:
            if self.plugin_class:
                result = self.func(get_plugin_instance(self.plugin_class), **kwargs)

            else:
                result = self.func(**kwargs)

            if inspect.iscoroutinefunction(self.func):
                assert inspect.iscoroutine(
                    result), "The task is defined as a coroutine function but does not return a coroutine"
                loop = asyncio.get_event_loop()
                if loop.is_closed():
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                result = loop.run_until_complete(result)
                loop.close()
        finally:
            stop = datetime.datetime.now()
            logger.info("End task %s after %s", self, stop - start)

        return result

    def get_parameters(self):
        """Returns a list of parameters"""
        if self.plugin_class is None:
            sig = inspect.signature(self.func)
            for index, parameter in enumerate(sig.parameters.values()):
                if not parameter.kind in [parameter.POSITIONAL_ONLY, parameter.KEYWORD_ONLY, parameter.POSITIONAL_OR_KEYWORD]:
                    raise RuntimeError("Task {} contains an unsupported {} parameter".format(parameter, parameter.kind))

                yield parameter

        else:
            var_keyword_seen = set()

            for cls in inspect.getmro(self.plugin_class):
                if issubclass(cls, BasePlugin) and hasattr(cls, self.func.__name__):
                    func = getattr(cls, self.func.__name__)
                    logger.debug("Found method %s from class %s", func, cls)
                    var_keyword_found = False
                    sig = inspect.signature(func)
                    for index, parameter in enumerate(sig.parameters.values()):
                        if index == 0:
                            # skip "self" parameter
                            continue

                        if parameter.kind == inspect.Parameter.VAR_KEYWORD:
                            # found "**kwargs" parameter.  we will continue to the next class in the mro
                            # to add any keyword parameters we have not yet used (i.e. whose name
                            # we have not yet seen)
                            var_keyword_found = True
                            continue

                        if parameter.kind in [parameter.POSITIONAL_ONLY, parameter.VAR_POSITIONAL]:
                            raise RuntimeError("Task {} contains an unsupported parameter \"{}\"".format(func, parameter))

                        if not parameter.name in var_keyword_seen:
                            var_keyword_seen.add(parameter.name)

                            logger.debug("Found parameter %s (%s)", parameter, parameter.kind)
                            yield parameter

                    # we only need to look at the next class in the mro
                    # when "**kwargs" is found
                    if not var_keyword_found:
                        break

    def get_configuration(self, key, default=None):
        """Returns the configuration for KEY"""
        if key in self.config:
            return self.config.get(key)
        else:
            return default

    def __str__(self):
        return self.qualified_name


def get_task_tree(white_list=None):
    """Returns a tree of Task instances

    The tree is comprised of dictionaries containing strings for
    keys and either dictionaries or Task instances for values.

    When WHITE_LIST is given, only the tasks and plugins in this
    list will become part of the task tree.  The WHITE_LIST may
    contain either strings, corresponding to the task of plugin
    __qualname__, or, preferable, the WHITE_LIST contains
    links to the task function or plugin class instead.
    """
    assert white_list is None or isinstance(white_list, list), type(white_list)

    if white_list is not None:
        white_list = set(item if isinstance(item, str) else item.__qualname__ for item in white_list)

    tree = dict((task.qualified_name, task)
                for task
                in _task_list.values()
                if white_list is None or task.qualified_name in white_list)

    plugins = get_plugin_list()
    for plugin in [plugin for plugin in plugins.values() if white_list is None or plugin.__qualname__ in white_list]:
        tasks = [func
                 for _, func
                 in inspect.getmembers(plugin)
                 if inspect.isfunction(func) and hasattr(func, "yaz_task_config")]
        if len(tasks) == 0:
            continue

        node = tree
        for name in plugin.__qualname__.split("."):
            if not name in node:
                node[name] = {}
            node = node[name]

        for func in tasks:
            logger.debug("Found task %s", func)
            node[func.__name__] = Task(plugin_class=plugin, func=func, config=func.yaz_task_config)

    return tree


@decorator
def task(func, **config):
    """Declare a function or method to be a Yaz task

    @yaz.task
    def talk(message: str = "Hello World!"):
        return message

    Or... group multiple tasks together

    class Tools(yaz.Plugin):
        @yaz.task
        def say(self, message: str = "Hello World!"):
            return message

        @yaz.task(option__choices=["A", "B", "C"])
        def choose(self, option: str = "A"):
            return option
    """
    if func.__name__ == func.__qualname__:
        assert not func.__qualname__ in _task_list, "Can not define the same task \"{}\" twice".format(func.__qualname__)
        logger.debug("Found task %s", func)
        _task_list[func.__qualname__] = Task(plugin_class=None, func=func, config=config)
    else:
        func.yaz_task_config = config

    return func
