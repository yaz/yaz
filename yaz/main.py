import sys

from .error import Error
from .loader import load
from .parser import Parser
from .task import get_task_tree


def main(argv=None, white_list=None, load_yaz_extension=True):
    assert argv is None or isinstance(argv, list), type(argv)
    assert white_list is None or isinstance(white_list, list), type(white_list)
    assert isinstance(load_yaz_extension, bool), type(load_yaz_extension)

    argv = sys.argv if argv is None else argv
    assert len(argv) > 0, len(argv)

    if load_yaz_extension:
        load("~/.yaz", "yaz_extension")

    parser = Parser(prog=argv[0])
    parser.add_task_tree(get_task_tree(white_list))

    task, kwargs = parser.parse_arguments(argv)

    if task:
        try:
            output = task(**kwargs)
            if isinstance(output, bool):
                code = 0 if output else 1
            elif isinstance(output, int):
                code = output % 256
            else:
                code = 0

        except Error as error:
            code = error.return_code
            output = error

    else:
        code = 0
        output = parser.format_help().rstrip()

    if output is not None:
        print(output)

    exit(code)
