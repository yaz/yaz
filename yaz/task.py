import re
import collections
import datetime
import functools
import inspect

from .decorator import decorator
from .plugin import Plugin

class Task:
    def __init__(self, plugin_class, func, config):
        assert plugin_class is None or issubclass(plugin_class, Plugin)
        assert callable(func)
        assert isinstance(config, dict)
        self.plugin_class = plugin_class
        self.plugin_instance = None
        self.func = func
        self.config = config

    def __call__(self, **kwargs):
        """Prepare dependencies and call this Task"""
        if self.plugin_class:
            if not self.plugin_instance:
                self.plugin_instance = self.plugin_class()
            return self.func(self.plugin_instance, **kwargs)

        else:
            return self.func(**kwargs)

    def get_parameters(self):
        """Returns a list of parameters"""
        sig = inspect.signature(self.func)
        for index, parameter in enumerate(sig.parameters.values()):
            if index == 0 and self.plugin_class is not None:
                # skip SELF parameter
                continue

            yield parameter

    def get_configuration(self, key, default = None):
        """Returns the configuration for KEY"""
        if key in self.config:
            value = self.config.get(key)

            if callable(value):
                return value(self)

            return value

        else:
            return default

    def get_documentation(self):
        """Returns a (short-doc, long-doc) tuple"""
        doc = inspect.getdoc(self.func)
        if doc:
            # long = self.yaz.render(doc, dict(plugin=plugin))
            long = doc
            match = re.match("^(?P<first_line>.+)\n?", long)
            if match:
                short = match.group("first_line")
            else:
                short = long
                long = ""
            return short.strip(), long.strip()
        return "", ""

    def __repr__(self):
        if self.plugin_class:
            return "<{self.__class__.__name__} {self.plugin_class.__qualname__}:{self.func.__qualname__}>".format(self=self)
        else:
            return "<{self.__class__.__name__} {self.func.__qualname__}>".format(self=self)

_task_list = {}

def get_task_tree():
    tree = _task_list.copy()

    plugins = Plugin.get_yaz_plugin_list()
    for plugin in plugins.values():
        node = tree
        for name in plugin.__qualname__.split("."):
            if not name in node:
                node[name] = {}
            node = node[name]

        for _, func in inspect.getmembers(plugin):
            if inspect.isfunction(func) and hasattr(func, "yaz_config"):
                node[func.__name__] = Task(plugin_class=plugin, func=func, config=func.yaz_config)

    return tree

@decorator
def task(func, **config):
    """Make a method into a Yaz task.

    @task
    def talk(message="Hello World!"):
        return message

    # Or... group multiple tasks together

    # class Tools(Yaz.Plugin):
    #     @task
    #     def say(self, message="Hello World!"):
    #         return message

    #     @task(choices=dict(option=["A", "B", "C"]))
    #     def choose(self, option="A"):
    #         return option
    """
    # @functools.wraps(func)
    # def wrapper(*args, **kwargs):
    #     return func(*args, **kwargs)
        # verbose = self.yaz.verbose
        # if verbose:
        #     start = datetime.datetime.now()
        #     print(self.render("{% color '', '', 'reverse' %}>>> {{ plugin.__class__.__name__ }} {{ task.__name__ }}{% endcolor %} {{ sourcefile }}",
        #                       dict(plugin=self, task=func, sourcefile=inspect.getsourcefile(func))))
        # try:
        #     return func(self, *args, **kwargs)
        # except Exception as exception:
        #     if verbose:
        #         print(self.render("{% color '', '', 'reverse' %}!!! {{ plugin.__class__.__name__ }} {{ exception }}{% endcolor %}",
        #                           dict(plugin=self, task=func, sourcefile=repr(exception))))
        #     raise
        # finally:
        #     if verbose:
        #         stop = datetime.datetime.now()
        #         print(self.render("{% color '', '', 'reverse' %}<<< {{ plugin.__class__.__name__ }} {{ task.__name__ }}{% endcolor %} {{ duration }}",
        #                           dict(plugin=self, task=func, duration=stop - start)))
    if func.__name__ == func.__qualname__:
        assert not func.__qualname__ in _task_list, "Can not define the same task {} twice".format(func.__qualname__)
        _task_list[func.__qualname__] = Task(plugin_class=None, func=func, config=config)
    else:
        func.yaz_config = config

    return func
