import sys
import unittest

from .log import logger
from .parser import Parser
from .task import get_task_tree

__all__ = ["TestCase"]


class TestCase(unittest.TestCase):
    """Helper class for building unit tests

    Many unit tests will need to simulate calling a task from
    the command line.  The `get_caller` method makes this easier.
    For example:

        import yaz
        import your_module

        class TestHelloWorld(yaz.TestCase):
            def test_010_greeting(self):
                caller = self.get_caller([your_module.task_or_plugin])
                self.assertEqual("Hello World!", caller("Hello World!")
    """

    def get_caller(self, white_list=None):
        def caller(*arguments):
            try:
                task, kwargs = parser.parse_arguments([sys.argv[0]] + list(arguments))
                logger.debug("Calling %s with %s", task, kwargs)

                self.assertTrue(callable(task), "The parser did not find a task")
                self.assertTrue(isinstance(kwargs, dict), "The parser did not find the parameters")
                return task(**kwargs)

            except SystemExit:
                parser.print_usage()
                raise

        parser = Parser()
        parser.add_task_tree(get_task_tree(white_list))

        return caller
