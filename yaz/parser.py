import argparse
import inspect
import re
import sys

class Parser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        kwargs["formatter_class"] = argparse.RawDescriptionHelpFormatter
        super().__init__(*args, **kwargs)

    def _format_name(self, name, prefix="", postfix=""):
        return "".join([prefix, name.replace("_", "-").lower(), postfix])

    def _add_task(self, parser, task):
        for parameter in task.get_parameters():
            parser.set_defaults(yaz_task=task)

            args = (self._format_name(parameter.name),)
            kwargs = {
                "help": task.get_configuration("{}__help".format(parameter.name)),
                "choices": task.get_configuration("{}__choices".format(parameter.name))
            }

            if parameter.default is not parameter.empty:
                args = (self._format_name(parameter.name, "-" if len(parameter.name) == 1 else "--"),)
                if not kwargs["help"]:
                    kwargs["help"] = "defaults to {}={!r}".format(parameter.name, parameter.default)
                kwargs["default"] = parameter.default
                kwargs["dest"] = parameter.name

            if parameter.annotation is not parameter.empty:
                if parameter.annotation is bool:
                    if parameter.default is parameter.empty:
                        group = parser.add_mutually_exclusive_group(required=True)
                        group.add_argument(
                            self._format_name(parameter.name, "-" if len(parameter.name) == 1 else "--"),
                            dest = parameter.name,
                            action="store_true",
                            help="{}, pass this flag to set to True".format(kwargs["help"])
                        )
                        group.add_argument(
                            self._format_name(parameter.name, "--no-"),
                            dest = parameter.name,
                            action="store_false",
                            help="{}, pass this flag to set to False".format(kwargs["help"])
                        )
                        continue

                    else:
                        if parameter.default:
                            args = (self._format_name(parameter.name, "--no-"),)
                            kwargs["action"] = "store_false"
                            kwargs["help"] = "{}, pass this flag to set to False".format(kwargs["help"])
                        else:
                            kwargs["action"] = "store_true"
                            kwargs["help"] = "{}, pass this flag to set to True".format(kwargs["help"])

                elif parameter.annotation is int:
                    kwargs["type"] = int

                elif parameter.annotation is float:
                    kwargs["type"] = float

            parser.add_argument(
                *args,
                **dict((key, value) for key, value in kwargs.items() if not value is None))

    def _add_task_tree_node(self, parser, task):
        if isinstance(task, dict) and len(task) == 1:
            task = next(iter(task.values()))

        if isinstance(task, dict):
            subparsers = parser.add_subparsers()
            for name, task in sorted(task.items()):
                self._add_task_tree_node(
                    subparsers.add_parser(self._format_name(name)),
                    task)

        else:
            self._add_task(parser, task)

    def add_task_tree(self, task_tree):
        assert isinstance(task_tree, dict)
        self._add_task_tree_node(self, task_tree)

    def parse_arguments(self, argv):
        assert isinstance(argv, list)
        assert all(isinstance(arg, str) for arg in argv)
        kwargs = vars(self.parse_args(argv))
        return kwargs.pop("yaz_task", None), kwargs
