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

    def testSingleFunction(self):
        """Should be available without specifying the task name"""
        parser = Parser()
        parser.add_task_tree(self._get_task_tree(["say"]))

        # without arguments, uses default value for message
        task, kwargs = parser.parse_arguments([])
        assert task(**kwargs) == "Hello World!"

        # provide message value as an argument
        task, kwargs = parser.parse_arguments([sys.argv[0], "--message", "I said HELLO!"])
        assert task(**kwargs) == "I said HELLO!"

    def testMultipleFunctions(self):
        """Should be available after specifying the task name"""
        parser = Parser()
        parser.add_task_tree(self._get_task_tree(["foo", "bar"]))

        # without arguments, can not determine the task to run
        task, kwargs = parser.parse_arguments([])
        assert task is None

        # provide the task as an argument
        task, kwargs = parser.parse_arguments([sys.argv[0], "foo"])
        assert task(**kwargs) == "Foo"

        # provide the task as an argument
        task, kwargs = parser.parse_arguments([sys.argv[0], "bar"])
        assert task(**kwargs) == "Bar"

    def testSingleMethod(self):
        """Should be available without specifying the plugin nor the task name"""
        parser = Parser()
        parser.add_task_tree(self._get_task_tree(["Person"]))

        # without arguments, can not determine the task to run
        task, kwargs = parser.parse_arguments([])
        assert task(**kwargs) == "I have very little to say."

    def testMultipleMethods(self):
        """Should be available without specifying the plugin name but after specifying the task name"""
        parser = Parser()
        parser.add_task_tree(self._get_task_tree(["Shape"]))

        # without arguments, can not determine the task to run
        task, kwargs = parser.parse_arguments([])
        assert task is None

        # provide the task as an argument
        task, kwargs = parser.parse_arguments([sys.argv[0], "circle"])
        assert task(**kwargs) == "Circle"

        # provide the task as an argument
        task, kwargs = parser.parse_arguments([sys.argv[0], "square"])
        assert task(**kwargs) == "Square"

    def testMultiplePlugins(self):
        """Should be available after specifying the plugin name and task name"""
        parser = Parser()
        parser.add_task_tree(self._get_task_tree(["Shape", "Person"]))

        # without arguments, can not determine the task to run
        task, kwargs = parser.parse_arguments([])
        assert task is None

        # provide the plugin as an argument (task name is not needed, as Person only has one task)
        task, kwargs = parser.parse_arguments([sys.argv[0], "person"])
        assert task(**kwargs) == "I have very little to say."

        # provide the plugin and task as an argument
        task, kwargs = parser.parse_arguments([sys.argv[0], "shape", "circle"])
        assert task(**kwargs) == "Circle"

        # provide the plugin and task as an argument
        task, kwargs = parser.parse_arguments([sys.argv[0], "shape", "square"])
        assert task(**kwargs) == "Square"

    def testNamingConvention(self):
        """Should convert Plugin and task name to conform with naming conventions"""
        parser = Parser()
        parser.add_task_tree(self._get_task_tree(["ThisWasCamelCase", "Person"]))

        task, kwargs = parser.parse_arguments([sys.argv[0], "this-was-camel-case", "this-was-underscored"])
        assert task(**kwargs) == "this-was-underscored"

        task, kwargs = parser.parse_arguments([sys.argv[0], "this-was-camel-case", "this-was-camel-case"])
        assert task(**kwargs) == "this-was-camel-case"

        task, kwargs = parser.parse_arguments([sys.argv[0], "this-was-camel-case", "this-was-also-underscored"])
        assert task(**kwargs) == "this-was-also-underscored"

    def testBooleanTypeAnnotation(self):
        """Should understand boolean type annotation"""
        parser = Parser()
        parser.add_task_tree(self._get_task_tree(["TypeAnnotation"]))

        task, kwargs = parser.parse_arguments([sys.argv[0], "required-boolean", "--check"])
        assert task(**kwargs) == True

        task, kwargs = parser.parse_arguments([sys.argv[0], "required-boolean", "--no-check"])
        assert task(**kwargs) == False

        task, kwargs = parser.parse_arguments([sys.argv[0], "optional-boolean-true"])
        assert task(**kwargs) == True

        task, kwargs = parser.parse_arguments([sys.argv[0], "optional-boolean-true", "--no-check"])
        assert task(**kwargs) == False

        task, kwargs = parser.parse_arguments([sys.argv[0], "optional-boolean-false"])
        assert task(**kwargs) == False

        task, kwargs = parser.parse_arguments([sys.argv[0], "optional-boolean-false", "--check"])
        assert task(**kwargs) == True

    def testIntegerTypeAnnotation(self):
        """Should understand integer type annotation"""
        parser = Parser()
        parser.add_task_tree(self._get_task_tree(["TypeAnnotation"]))

        task, kwargs = parser.parse_arguments([sys.argv[0], "required-integer", "123"])
        assert task(**kwargs) == 123

        task, kwargs = parser.parse_arguments([sys.argv[0], "optional-integer"])
        assert task(**kwargs) == 42

        task, kwargs = parser.parse_arguments([sys.argv[0], "optional-integer", "--number", "123"])
        assert task(**kwargs) == 123

    def testFloatTypeAnnotation(self):
        """Should understand float type annotation"""
        parser = Parser()
        parser.add_task_tree(self._get_task_tree(["TypeAnnotation"]))

        task, kwargs = parser.parse_arguments([sys.argv[0], "required-float", "0.5"])
        assert task(**kwargs) == 0.5

        task, kwargs = parser.parse_arguments([sys.argv[0], "optional-float"])
        assert task(**kwargs) == 3.14

        task, kwargs = parser.parse_arguments([sys.argv[0], "optional-float", "--number", "0.5"])
        assert task(**kwargs) == 0.5
