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
            result = task(**kwargs)

            # when the result is a boolean, exit with 0 (success) or 1 (failure)
            if isinstance(result, bool):
                code = 0 if result else 1
                output = None

            # when the result is an integer, exit with that integer value
            elif isinstance(result, int):
                code = result % 256
                output = None

            # otherwise exit with 0 (success) and print the result
            else:
                code = 0
                output = result

        # when yaz.Error occurs, exit with the given return code and print the error message
        # when any other error occurs, let python handle the exception (i.e. exit(1) and print call stack)
        except Error as error:
            code = error.return_code
            output = error

    else:
        # when no task is found to execute, exit with 1 (failure) and print the help text
        code = 1
        output = parser.format_help().rstrip()

    if output is not None:
        print(output)

    sys.exit(code)
