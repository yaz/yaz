import argparse
import re

__all__ = ["Parser"]


class Parser(argparse.ArgumentParser):
    """Yaz specific ArgumentParser

    Given a collection of yaz.tasks, an ArgumentParser is
    constructed.  This ArgumentParser will subsequently be
    used to handle arguments from the command line.
    """

    def __init__(self, *args, **kwargs):
        kwargs["formatter_class"] = argparse.RawDescriptionHelpFormatter
        super().__init__(*args, **kwargs)

    def _format_name(self, name: str, prefix_short: str = "", prefix_long: str = ""):
        # todo: cleanup below code.  it does what it needs to do, but is not very pretty
        name = re.sub(r"([^A-Z]+)([A-Z]+)", r"\1-\2", name)
        name = re.sub(r"_", r"-", name)
        name = re.sub(r"-[-]+", r"-", name)
        name = re.sub(r"^[-]+", r"", name)
        name = re.sub(r"[-]+$", r"", name)

        if len(name) == 1:
            return "".join([prefix_short, name.lower()])

        elif len(name) > 1:
            return "".join([prefix_long, name.lower()])

        else:
            return ""

    def _add_task(self, parser, task):
        if __debug__:
            from .task import Task
            assert isinstance(parser, Parser), type(parser)
            assert isinstance(task, Task), type(task)

        # get all parameters with their formatted name
        parameters = [(index if parameter.default is parameter.empty else 999, self._format_name(parameter.name), parameter)
                      for index, parameter
                      in enumerate(task.get_parameters())]

        # sort all parameters, either by their index (for required parameters) or their name (for optional parameters)
        parameters = sorted(parameters)

        parameter_map = {}

        for index, formatted_name, parameter in parameters:
            args = (formatted_name,)
            kwargs = {
                "help": task.get_configuration("{}__help".format(parameter.name)),
                "choices": task.get_configuration("{}__choices".format(parameter.name)),
            }

            if parameter.default is not parameter.empty:
                args = (self._format_name(parameter.name, "-", "--"),)
                if not kwargs["help"]:
                    kwargs["help"] = "defaults to {}={!r}".format(parameter.name, parameter.default)
                kwargs["dest"] = parameter.name
                parser.set_defaults(**{parameter.name: parameter.default})

            type_ = task.get_configuration("{}__type".format(parameter.name), str if parameter.annotation is parameter.empty else parameter.annotation)
            if type_ is bool:
                group = parser.add_mutually_exclusive_group(required=parameter.default is parameter.empty)
                group.add_argument(
                    self._format_name(parameter.name, "-", "--"),
                    dest=parameter.name,
                    action="store_true",
                    help="{}, pass this flag to set to True".format(kwargs["help"]) if kwargs["help"] else "pass this flag to set to True"
                )
                group.add_argument(
                    self._format_name(parameter.name, "--no-", "--no-"),
                    dest=parameter.name,
                    action="store_false",
                    help="{}, pass this flag to set to False".format(kwargs["help"]) if kwargs["help"] else "pass this flag to set to False"
                )
                continue

            elif callable(type_):
                kwargs["type"] = type_

            else:
                raise RuntimeError("Task \"{}\" defines parameter \"{}\" with an unknown type \"{}\"".format(task, parameter, type_))

            parameter_map.update({arg: parameter.name for arg in args})
            parser.add_argument(
                *args,
                **dict((key, value) for key, value in kwargs.items() if not value is None))

        parser.description = task.documentation.full
        parser.set_defaults(yaz_task=task)
        parser.set_defaults(yaz_parameter_map=parameter_map)

    def _get_plugin_documentation(self, tasks):
        if not tasks:
            return

        first_task = tasks[0][1]
        if isinstance(first_task, dict):
            return

        docs = [first_task.plugin_documentation.full, ""]
        max_name_length = max(len(name) for name, _ in tasks)
        docs.extend("{:{length}}  {}".format(self._format_name(name), task.documentation.short, length=max_name_length) for name, task in tasks)
        return "\n".join(docs)

    def _add_task_tree_node(self, parser, task):
        while isinstance(task, dict) and len(task) == 1:
            task = next(iter(task.values()))

        if isinstance(task, dict):
            tasks = sorted(task.items())
            subparsers = parser.add_subparsers(description=self._get_plugin_documentation(tasks))
            for name, task in tasks:
                self._add_task_tree_node(
                    subparsers.add_parser(self._format_name(name)),
                    task)

        else:
            self._add_task(parser, task)

    def add_task_tree(self, task_tree):
        assert isinstance(task_tree, dict), type(task_tree)
        self._add_task_tree_node(self, task_tree)

    def parse_arguments(self, argv):
        assert isinstance(argv, list), type(argv)
        assert all(isinstance(arg, str) for arg in argv), [type(arg) for arg in argv]
        kwargs = vars(self.parse_args(argv[1:]))
        task = kwargs.pop("yaz_task", None)

        # use the parameter_map to get the original parameter names instead
        # of the names used by the argument parser
        parameter_map = kwargs.pop("yaz_parameter_map", None)
        if parameter_map:
            kwargs = {parameter_map.get(key, key): value for key, value in kwargs.items()}

        return task, kwargs
