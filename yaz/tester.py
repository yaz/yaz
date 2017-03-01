import sys
import unittest

from yaz.parser import Parser
from yaz.task import get_task_tree

from .log import logger


class TestCase(unittest.TestCase):
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
