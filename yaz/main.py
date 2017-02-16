import sys

from .loader import load
from .parser import Parser
from .task import get_task_tree


def main(argv=None, white_list=None, load_yaz_extension=True):
    assert argv is None or isinstance(argv, list), type(argv)
    assert white_list is None or isinstance(white_list, list), type(white_list)
    assert isinstance(load_yaz_extension, bool), type(load_yaz_extension)

    if load_yaz_extension:
        load("~/.yaz", "yaz_extension")

    parser = Parser()
    parser.add_task_tree(get_task_tree(white_list))

    task, kwargs = parser.parse_arguments(sys.argv if argv is None else argv)
    if task:
        result = task(**kwargs)
        if result is not None:
            print(result)

        if isinstance(result, int) and not isinstance(result, bool):
            exit(result)

        return result

    else:
        parser.print_help()
