import re
import inspect
import asyncio

from .decorator import decorator
from .plugin import BasePlugin, get_plugin_instance, get_plugin_list


class Task:
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
        return self.Documentation(inspect.getdoc(self.plugin_class))

    @property
    def documentation(self):
        return self.Documentation(inspect.getdoc(self.func))

    def __call__(self, **kwargs):
        """Prepare dependencies and call this Task"""
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

        return result

    def get_qualified_name(self):
        """Returns the __qualname__ of this Task"""
        return self.func.__qualname__

    def get_parameters(self):
        """Returns a list of parameters"""
        sig = inspect.signature(self.func)
        for index, parameter in enumerate(sig.parameters.values()):
            if index == 0 and self.plugin_class is not None:
                # skip SELF parameter
                continue

            yield parameter

    def get_configuration(self, key, default=None):
        """Returns the configuration for KEY"""
        if key in self.config:
            return self.config.get(key)
        else:
            return default

    def __str__(self):
        return self.get_qualified_name()


_task_list = {}


def get_task_tree(white_list=None):
    assert white_list is None or isinstance(white_list, list), type(white_list)

    if white_list is not None:
        white_list = set(item if isinstance(item, str) else item.__qualname__ for item in white_list)

    tree = dict((task.get_qualified_name(), task)
                for task
                in _task_list.values()
                if white_list is None or task.get_qualified_name() in white_list)

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
            node[func.__name__] = Task(plugin_class=plugin, func=func, config=func.yaz_task_config)

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
        func.yaz_task_config = config

    return func
