import unittest
import sys

from ..yaz.loader import load
from ..yaz.parser import Parser
from ..yaz.task import get_task_tree

import test.extension.singlefunction
import test.extension.multiplefunctions
import test.extension.singlemethod
import test.extension.multiplemethods
import test.extension.namingconvention
import test.extension.typeannotation

class TestParser(unittest.TestCase):
    def _get_task_tree(self, white_list):
        """Helper function to only get specific tasks needed for a test"""
        return dict(
            (qualname, task)
            for qualname, task
            in get_task_tree().items()
            if qualname in white_list)

    def test_single_function(self):
        """Should be available without specifying the task name"""
        parser = Parser()
        parser.add_task_tree(self._get_task_tree(["say"]))

        # without arguments, uses default value for message
        task, kwargs = parser.parse_arguments([])
        self.assertEqual("Hello World!", task(**kwargs))

        # provide message value as an argument
        task, kwargs = parser.parse_arguments([sys.argv[0], "--message", "I said HELLO!"])
        self.assertEqual("I said HELLO!", task(**kwargs))

    def test_multiple_functions(self):
        """Should be available after specifying the task name"""
        parser = Parser()
        parser.add_task_tree(self._get_task_tree(["foo", "bar"]))

        # without arguments, can not determine the task to run
        task, kwargs = parser.parse_arguments([])
        self.assertIsNone(task)

        # provide the task as an argument
        task, kwargs = parser.parse_arguments([sys.argv[0], "foo"])
        self.assertEqual("Foo", task(**kwargs))

        # provide the task as an argument
        task, kwargs = parser.parse_arguments([sys.argv[0], "bar"])
        self.assertEqual("Bar", task(**kwargs))

    def test_single_method(self):
        """Should be available without specifying the plugin nor the task name"""
        parser = Parser()
        parser.add_task_tree(self._get_task_tree(["Person"]))

        # without arguments, can not determine the task to run
        task, kwargs = parser.parse_arguments([])
        self.assertEqual("I have very little to say.", task(**kwargs))

    def test_multiple_methods(self):
        """Should be available without specifying the plugin name but after specifying the task name"""
        parser = Parser()
        parser.add_task_tree(self._get_task_tree(["Shape"]))

        # without arguments, can not determine the task to run
        task, kwargs = parser.parse_arguments([])
        self.assertIsNone(task)

        # provide the task as an argument
        task, kwargs = parser.parse_arguments([sys.argv[0], "circle"])
        self.assertEqual("Circle", task(**kwargs))

        # provide the task as an argument
        task, kwargs = parser.parse_arguments([sys.argv[0], "square"])
        self.assertEqual("Square", task(**kwargs))

    def test_multiple_plugins(self):
        """Should be available after specifying the plugin name and task name"""
        parser = Parser()
        parser.add_task_tree(self._get_task_tree(["Shape", "Person"]))

        # without arguments, can not determine the task to run
        task, kwargs = parser.parse_arguments([])
        self.assertIsNone(task)

        # provide the plugin as an argument (task name is not needed, as Person only has one task)
        task, kwargs = parser.parse_arguments([sys.argv[0], "person"])
        self.assertEqual("I have very little to say.", task(**kwargs))

        # provide the plugin and task as an argument
        task, kwargs = parser.parse_arguments([sys.argv[0], "shape", "circle"])
        self.assertEqual("Circle", task(**kwargs))

        # provide the plugin and task as an argument
        task, kwargs = parser.parse_arguments([sys.argv[0], "shape", "square"])
        self.assertEqual("Square", task(**kwargs))

    def test_naming_convention(self):
        """Should convert Plugin and task name to conform with naming conventions"""
        parser = Parser()
        parser.add_task_tree(self._get_task_tree(["ThisWasCamelCase", "Person"]))

        task, kwargs = parser.parse_arguments([sys.argv[0], "this-was-camel-case", "this-was-underscored"])
        self.assertEqual("this-was-underscored", task(**kwargs))

        task, kwargs = parser.parse_arguments([sys.argv[0], "this-was-camel-case", "this-was-camel-case"])
        self.assertEqual("this-was-camel-case", task(**kwargs))

        task, kwargs = parser.parse_arguments([sys.argv[0], "this-was-camel-case", "this-was-also-underscored"])
        self.assertEqual("this-was-also-underscored", task(**kwargs))

    def test_boolean_type_annotation(self):
        """Should understand boolean type annotation"""
        parser = Parser()
        parser.add_task_tree(self._get_task_tree(["TypeAnnotation"]))

        task, kwargs = parser.parse_arguments([sys.argv[0], "required-boolean", "--check"])
        self.assertTrue(task(**kwargs))

        task, kwargs = parser.parse_arguments([sys.argv[0], "required-boolean", "--no-check"])
        self.assertFalse(task(**kwargs))

        task, kwargs = parser.parse_arguments([sys.argv[0], "optional-boolean-true"])
        self.assertTrue(task(**kwargs))

        task, kwargs = parser.parse_arguments([sys.argv[0], "optional-boolean-true", "--no-check"])
        self.assertFalse(task(**kwargs))

        task, kwargs = parser.parse_arguments([sys.argv[0], "optional-boolean-false"])
        self.assertFalse(task(**kwargs))

        task, kwargs = parser.parse_arguments([sys.argv[0], "optional-boolean-false", "--check"])
        self.assertTrue(task(**kwargs))

    def test_integer_type_annotation(self):
        """Should understand integer type annotation"""
        parser = Parser()
        parser.add_task_tree(self._get_task_tree(["TypeAnnotation"]))

        task, kwargs = parser.parse_arguments([sys.argv[0], "required-integer", "123"])
        self.assertEqual(123, task(**kwargs))

        task, kwargs = parser.parse_arguments([sys.argv[0], "optional-integer"])
        self.assertEqual(42, task(**kwargs))

        task, kwargs = parser.parse_arguments([sys.argv[0], "optional-integer", "--number", "123"])
        self.assertEqual(123, task(**kwargs))

    def test_float_type_annotation(self):
        """Should understand float type annotation"""
        parser = Parser()
        parser.add_task_tree(self._get_task_tree(["TypeAnnotation"]))

        task, kwargs = parser.parse_arguments([sys.argv[0], "required-float", "0.5"])
        self.assertEqual(0.5, task(**kwargs))
        assert task(**kwargs) == 0.5

        task, kwargs = parser.parse_arguments([sys.argv[0], "optional-float"])
        self.assertEqual(3.14, task(**kwargs))

        task, kwargs = parser.parse_arguments([sys.argv[0], "optional-float", "--number", "0.5"])
        self.assertEqual(0.5, task(**kwargs))
