import re
import collections
import datetime
import functools
import inspect

from .decorator import decorator

class Task:
    def __init__(self, parent, func, config):
        assert parent is None
        assert callable(func)
        assert isinstance(config, dict)
        self.parent = parent
        self.func = func
        self.config = config

    def get(self, key, default = None):
        """Returns the configuration for KEY"""
        if key in self.config:
            value = self.config.get(key)

            if callable(value):
                return value(self)

            return value

        else:
            return default

    def __call__(self, **kwargs):
        """Prepare dependencies and call this Task"""
        # todo: prepare dependencies
        return self.func(**kwargs)

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
        if self.parent:
            return "<{self.__class__.__name__} \"{self.parent.__class__.__name__}.{self.func.__name__}\">".format(self=self)
        else:
            return "<{self.__class__.__name__} \"{self.func.__name__}\">".format(self=self)

_task_tree = {}

def get_task_tree():
    return _task_tree

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
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
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
    # wrapper.yaz_config = config
    _task_tree[func.__name__] = Task(parent=None, func=wrapper, config=config)
    return wrapper
