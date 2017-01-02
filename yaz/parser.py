import argparse
import inspect
import re
import sys

class Parser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        kwargs["formatter_class"] = argparse.RawDescriptionHelpFormatter
        super().__init__(*args, **kwargs)

    def _add_task(self, parser, task):
        sig = inspect.signature(task.func)
        for index, parameter in enumerate(sig.parameters.values()):
            if index == 0 and not task.plugin is None:
                # skip SELF parameter
                continue

            name = parameter.name.replace("_", "-")
            kwargs = {}
            if parameter.default is parameter.empty:
                # this parameter is required
                args = (name,)
                kwargs["help"] = task.get("{}__help".format(parameter.name))
                kwargs["default"] = task.get("{}__default".format(parameter.name))
                kwargs["choices"] = task.get("{}__choices".format(parameter.name))
            else:
                # this parameter is optional
                if len(name) == 1:
                    args = ("-{}".format(name), "--{}".format(name))
                else:
                    args = ("--{}".format(name),)

                kwargs["default"] = task.get("{}__default".format(parameter.name), parameter.default)
                kwargs["help"] = task.get("{}__help".format(parameter.name), "defaults to {}={!r}".format(parameter.name, kwargs["default"]))
                kwargs["choices"] = task.get("{}__choices".format(parameter.name))
                kwargs["dest"] = parameter.name
                if isinstance(parameter.default, bool):
                    if parameter.default:
                        args = ("--no-{}".format(name),)
                        kwargs["action"] = "store_false"
                        kwargs["help"] = "{}, pass this flag to set to False".format(kwargs["help"])
                    else:
                        kwargs["action"] = "store_true"
                        kwargs["help"] = "{}, pass this flag to set to True".format(kwargs["help"])
                elif isinstance(parameter.default, int):
                    kwargs["type"] = int
                elif isinstance(parameter.default, float):
                    kwargs["type"] = float

            parser.set_defaults(yaz_task=task)
            parser.add_argument(
                *args,
                **dict((key, value) for key, value in kwargs.items() if not value is None))

    def _add_task_tree_node(self, parser, task):
        if isinstance(task, dict) and len(task) == 1:
            task = next(iter(task.values()))

        if isinstance(task, dict):
            subparsers = parser.add_subparsers()
            for name, task in task.items():
                self._add_task_tree_node(
                    subparsers.add_parser(name.lower()),
                    task)

        else:
            self._add_task(parser, task)

    def add_task_tree(self, task_tree):
        assert isinstance(task_tree, dict)
        self._add_task_tree_node(self, task_tree)

    def parse_arguments(self, argv):
        assert isinstance(argv, list)
        kwargs = vars(self.parse_args(argv))
        return kwargs.pop("yaz_task", None), kwargs
