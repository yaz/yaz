import sys

from .loader import load
from .parser import Parser
from .task import get_task_tree


def main(argv=None, load_yaz_extension=True):
    if load_yaz_extension:
        load("~/.yaz", "yaz_extension")

    parser = Parser()
    parser.add_task_tree(get_task_tree())

    task, kwargs = parser.parse_arguments(sys.argv if argv is None else argv)
    if task:
        result = task(**kwargs)
        if result is not None:
            print(result)

    else:
        parser.print_help()
