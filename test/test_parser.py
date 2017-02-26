import os.path
import sys
import unittest

from yaz.parser import Parser
from yaz.task import get_task_tree

# The following imports are needed, as they declare the functions and classes needed by the tests
import test.extension.singlefunction
import test.extension.multiplefunctions
import test.extension.singlemethod
import test.extension.multiplemethods
import test.extension.namingconvention
import test.extension.typeannotation
import test.extension.taskconfiguration


class TestParser(unittest.TestCase):
    def test_010_single_function(self):
        """Should be available without specifying the task name"""
        parser = Parser()
        parser.add_task_tree(get_task_tree(["say"]))

        # without arguments, uses default value for message
        task, kwargs = parser.parse_arguments([])
        self.assertEqual("Hello World!", task(**kwargs))

        # provide message value as an argument
        task, kwargs = parser.parse_arguments([sys.argv[0], "--message", "I said HELLO!"])
        self.assertEqual("I said HELLO!", task(**kwargs))

    def test_020_multiple_functions(self):
        """Should be available after specifying the task name"""
        parser = Parser()
        parser.add_task_tree(get_task_tree(["foo", "bar"]))

        # without arguments, can not determine the task to run
        task, kwargs = parser.parse_arguments([])
        self.assertIsNone(task)

        # provide the task as an argument
        task, kwargs = parser.parse_arguments([sys.argv[0], "foo"])
        self.assertEqual("Foo", task(**kwargs))

        # provide the task as an argument
        task, kwargs = parser.parse_arguments([sys.argv[0], "bar"])
        self.assertEqual("Bar", task(**kwargs))

    def test_030_single_method(self):
        """Should be available without specifying the plugin nor the task name"""
        parser = Parser()
        parser.add_task_tree(get_task_tree(["Person"]))

        # without arguments, can not determine the task to run
        task, kwargs = parser.parse_arguments([])
        self.assertEqual("I have very little to say.", task(**kwargs))

    def test_040_multiple_methods(self):
        """Should be available without specifying the plugin name but after specifying the task name"""
        parser = Parser()
        parser.add_task_tree(get_task_tree(["Shape"]))

        # without arguments, can not determine the task to run
        task, kwargs = parser.parse_arguments([])
        self.assertIsNone(task)

        # provide the task as an argument
        task, kwargs = parser.parse_arguments([sys.argv[0], "circle"])
        self.assertEqual("Circle", task(**kwargs))

        # provide the task as an argument
        task, kwargs = parser.parse_arguments([sys.argv[0], "square"])
        self.assertEqual("Square", task(**kwargs))

    def test_050_multiple_plugins(self):
        """Should be available after specifying the plugin name and task name"""
        parser = Parser()
        parser.add_task_tree(get_task_tree(["Shape", "Person"]))

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

    def test_060_naming_convention(self):
        """Should convert Plugin name, task name, and argument name to conform with naming conventions"""
        parser = Parser()
        parser.add_task_tree(get_task_tree(["ThisWasCamelCase", "Person"]))

        task, kwargs = parser.parse_arguments([sys.argv[0], "this-was-camel-case", "this-was-underscored"])
        self.assertEqual("this-was-underscored", task(**kwargs))

        task, kwargs = parser.parse_arguments([sys.argv[0], "this-was-camel-case", "this-was-camel-case"])
        self.assertEqual("this-was-camel-case", task(**kwargs))

        task, kwargs = parser.parse_arguments([sys.argv[0], "this-was-camel-case", "this-was-also-underscored"])
        self.assertEqual("this-was-also-underscored", task(**kwargs))

        task, kwargs = parser.parse_arguments([sys.argv[0], "this-was-camel-case", "required-arguments", "a", "b", "c", "d"])
        self.assertEqual(("a", "b", "c", "d"), task(**kwargs))

        task, kwargs = parser.parse_arguments([sys.argv[0], "this-was-camel-case", "optional-arguments"])
        self.assertEqual(("A", "B", "C", "D"), task(**kwargs))

    def test_070_string_type_annotation(self):
        """Should understand string type annotation"""
        parser = Parser()
        parser.add_task_tree(get_task_tree(["TypeAnnotation"]))

        task, kwargs = parser.parse_arguments([sys.argv[0], "required-string", "Hello World"])
        self.assertEqual("Hello World", task(**kwargs))

        task, kwargs = parser.parse_arguments([sys.argv[0], "optional-string", "--string=Alternative"])
        self.assertEqual("Alternative", task(**kwargs))

        task, kwargs = parser.parse_arguments([sys.argv[0], "optional-string"])
        self.assertEqual("Hello World!", task(**kwargs))

    def test_075_boolean_type_annotation(self):
        """Should understand boolean type annotation"""
        parser = Parser()
        parser.add_task_tree(get_task_tree(["TypeAnnotation"]))

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

    def test_080_integer_type_annotation(self):
        """Should understand integer type annotation"""
        parser = Parser()
        parser.add_task_tree(get_task_tree(["TypeAnnotation"]))

        task, kwargs = parser.parse_arguments([sys.argv[0], "required-integer", "123"])
        self.assertEqual(123, task(**kwargs))

        task, kwargs = parser.parse_arguments([sys.argv[0], "optional-integer"])
        self.assertEqual(42, task(**kwargs))

        task, kwargs = parser.parse_arguments([sys.argv[0], "optional-integer", "--number", "123"])
        self.assertEqual(123, task(**kwargs))

    def test_090_float_type_annotation(self):
        """Should understand float type annotation"""
        parser = Parser()
        parser.add_task_tree(get_task_tree(["TypeAnnotation"]))

        task, kwargs = parser.parse_arguments([sys.argv[0], "required-float", "0.5"])
        self.assertEqual(0.5, task(**kwargs))

        task, kwargs = parser.parse_arguments([sys.argv[0], "optional-float"])
        self.assertEqual(3.14, task(**kwargs))

        task, kwargs = parser.parse_arguments([sys.argv[0], "optional-float", "--number", "0.5"])
        self.assertEqual(0.5, task(**kwargs))

    def test_095_file_type_annotation(self):
        """Should understand file, i.e. open, type annotation"""
        parser = Parser()
        parser.add_task_tree(get_task_tree(["TypeAnnotation"]))

        task, kwargs = parser.parse_arguments([sys.argv[0], "required-file", os.path.join(os.path.dirname(__file__), "file_type_annotation/input.txt")])
        self.assertEqual("First line\nSecond line\nThird line", task(**kwargs))

        task, kwargs = parser.parse_arguments([sys.argv[0], "optional-file", "--file", os.path.join(os.path.dirname(__file__), "file_type_annotation/input.txt")])
        self.assertEqual("First line\nSecond line\nThird line", task(**kwargs))

        expected = "#!/usr/bin/env python3"
        task, kwargs = parser.parse_arguments([sys.argv[0], "optional-file", "--length", str(len(expected))])
        self.assertEqual(expected, task(**kwargs))

    def test_100_choices_configuration(self):
        """Should accept predefined choices"""
        parser = Parser()
        parser.add_task_tree(get_task_tree(["ConfigurationPlugin"]))

        # using available choice
        task, kwargs = parser.parse_arguments([sys.argv[0], "required-choice", "yes"])
        self.assertTrue(task(**kwargs))

        # using unavailable choice
        self.assertRaises(SystemExit, parser.parse_arguments, [sys.argv[0], "required-choice", "unavailable"])
