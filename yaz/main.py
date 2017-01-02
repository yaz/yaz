import sys

from .parser import Parser
from .task import get_task_tree

def main():
    parser = Parser()
    parser.add_task_tree(get_task_tree())

    task, kwargs = parser.parse_arguments(sys.argv[1:])
    if task:
        result = task(**kwargs)
        if result is not None:
            print(result)
