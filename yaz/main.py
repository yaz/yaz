import sys

from .task import get_task_tree
from .plugin import Plugin
from .parser import Parser

def main():
    parser = Parser()
    parser.add_task_tree(get_task_tree())

    task, kwargs = parser.parse_arguments(sys.argv[1:])
    if task:
        print(task(**kwargs))
