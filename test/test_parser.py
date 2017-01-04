import unittest

from ..yaz.task import get_task_tree
from ..yaz.parser import Parser

import test.singlefunction
import test.multiplefunctions
import test.singlemethod
import test.multiplemethods
import test.namingconvention
import test.typeannotation

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
        task, kwargs = parser.parse_arguments(["--message", "I said HELLO!"])
        assert task(**kwargs) == "I said HELLO!"

    def testMultipleFunctions(self):
        """Should be available after specifying the task name"""
        parser = Parser()
        parser.add_task_tree(self._get_task_tree(["foo", "bar"]))

        # without arguments, can not determine the task to run
        task, kwargs = parser.parse_arguments([])
        assert task is None

        # provide the task as an argument
        task, kwargs = parser.parse_arguments(["foo"])
        assert task(**kwargs) == "Foo"

        # provide the task as an argument
        task, kwargs = parser.parse_arguments(["bar"])
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
        task, kwargs = parser.parse_arguments(["circle"])
        assert task(**kwargs) == "Circle"

        # provide the task as an argument
        task, kwargs = parser.parse_arguments(["square"])
        assert task(**kwargs) == "Square"

    def testMultiplePlugins(self):
        """Should be available after specifying the plugin name and task name"""
        parser = Parser()
        parser.add_task_tree(self._get_task_tree(["Shape", "Person"]))

        # without arguments, can not determine the task to run
        task, kwargs = parser.parse_arguments([])
        assert task is None

        # provide the plugin as an argument (task name is not needed, as Person only has one task)
        task, kwargs = parser.parse_arguments(["person"])
        assert task(**kwargs) == "I have very little to say."

        # provide the plugin and task as an argument
        task, kwargs = parser.parse_arguments(["shape", "circle"])
        assert task(**kwargs) == "Circle"

        # provide the plugin and task as an argument
        task, kwargs = parser.parse_arguments(["shape", "square"])
        assert task(**kwargs) == "Square"

    def testNamingConvention(self):
        """Should convert Plugin and task name to conform with naming conventions"""
        parser = Parser()
        parser.add_task_tree(self._get_task_tree(["ThisWasCamelCase", "Person"]))

        task, kwargs = parser.parse_arguments(["this-was-camel-case", "this-was-underscored"])
        assert task(**kwargs) == "this-was-underscored"

        task, kwargs = parser.parse_arguments(["this-was-camel-case", "this-was-camel-case"])
        assert task(**kwargs) == "this-was-camel-case"

        task, kwargs = parser.parse_arguments(["this-was-camel-case", "this-was-also-underscored"])
        assert task(**kwargs) == "this-was-also-underscored"

    def testBooleanTypeAnnotation(self):
        """Should understand boolean type annotation"""
        parser = Parser()
        parser.add_task_tree(self._get_task_tree(["TypeAnnotation"]))

        task, kwargs = parser.parse_arguments(["required-boolean", "--check"])
        assert task(**kwargs) == True

        task, kwargs = parser.parse_arguments(["required-boolean", "--no-check"])
        assert task(**kwargs) == False

        task, kwargs = parser.parse_arguments(["optional-boolean-true"])
        assert task(**kwargs) == True

        task, kwargs = parser.parse_arguments(["optional-boolean-true", "--no-check"])
        assert task(**kwargs) == False

        task, kwargs = parser.parse_arguments(["optional-boolean-false"])
        assert task(**kwargs) == False

        task, kwargs = parser.parse_arguments(["optional-boolean-false", "--check"])
        assert task(**kwargs) == True

    def testIntegerTypeAnnotation(self):
        """Should understand integer type annotation"""
        parser = Parser()
        parser.add_task_tree(self._get_task_tree(["TypeAnnotation"]))

        task, kwargs = parser.parse_arguments(["required-integer", "123"])
        assert task(**kwargs) == 123

        task, kwargs = parser.parse_arguments(["optional-integer"])
        assert task(**kwargs) == 42

        task, kwargs = parser.parse_arguments(["optional-integer", "--number", "123"])
        assert task(**kwargs) == 123

    def testFloatTypeAnnotation(self):
        """Should understand float type annotation"""
        parser = Parser()
        parser.add_task_tree(self._get_task_tree(["TypeAnnotation"]))

        task, kwargs = parser.parse_arguments(["required-float", "0.5"])
        assert task(**kwargs) == 0.5

        task, kwargs = parser.parse_arguments(["optional-float"])
        assert task(**kwargs) == 3.14

        task, kwargs = parser.parse_arguments(["optional-float", "--number", "0.5"])
        assert task(**kwargs) == 0.5
