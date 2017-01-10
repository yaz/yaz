import importlib
import os.path
import sys


def load(directory_name, module_name):
    """Try to load and return a module

    Will add DIRECTORY_NAME to sys.path and tries to import MODULE_NAME.

    For example:
    load("~/.yaz", "yaz_extension")
    """
    directory_name = os.path.expanduser(directory_name)
    if os.path.isdir(directory_name) and directory_name not in sys.path:
        sys.path.append(directory_name)

    try:
        return importlib.import_module(module_name)
    except ImportError:
        pass
