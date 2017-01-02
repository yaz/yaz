import sys

from .task import get_task_tree
from .plugin import Plugin
from .parser import Parser

def main():
    # tasks = get_task_list()
    # print(tasks)

    tasks = get_task_tree()
    print(tasks)

    # plugins = Plugin.get_yaz_plugin_list()
    # print(plugins)

    parser = Parser()
    # print(parser)

    parser.add_task_tree(tasks)
    task, kwargs = parser.parse_arguments(sys.argv[1:])
    print(task, kwargs)

    if task:
        print(task(**kwargs))

    print("--------------------------------------------------------------------------------")
