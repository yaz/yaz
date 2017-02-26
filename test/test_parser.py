import os.path
import yaz

import test.extension.singlefunction as single_function
import test.extension.multiplefunctions as multiple_functions
import test.extension.singlemethod as single_method
import test.extension.multiplemethods as multiple_methods
import test.extension.namingconvention as naming_convention
import test.extension.typeannotation as type_annotation
import test.extension.taskconfiguration as task_configuration


class TestParser(yaz.TestCase):
    def test_010_single_function(self):
        """Should be available without specifying the task name"""
        caller = self.get_caller([single_function.say])

        # without arguments, uses default value for message
        self.assertEqual("Hello World!", caller())

        # provide message value as an argument
        self.assertEqual("I said HELLO!", caller("--message", "I said HELLO!"))

    def test_020_multiple_functions(self):
        """Should be available after specifying the task name"""
        caller = self.get_caller([multiple_functions.foo, multiple_functions.bar])

        # without arguments, can not determine the task to run
        with self.assertRaisesRegex(AssertionError, "The parser did not find a task"):
            caller()

        # provide the task as an argument
        self.assertEqual("Foo", caller("foo"))

        # provide the task as an argument
        self.assertEqual("Bar", caller("bar"))

    def test_030_single_method(self):
        """Should be available without specifying the plugin nor the task name"""
        caller = self.get_caller([single_method.Person])
        self.assertEqual("I have very little to say.", caller())

    def test_040_multiple_methods(self):
        """Should be available without specifying the plugin name but after specifying the task name"""
        caller = self.get_caller([multiple_methods.Shape])

        # without arguments, can not determine the task to run
        with self.assertRaisesRegex(AssertionError, "The parser did not find a task"):
            caller()

        # provide the task as an argument
        self.assertEqual("Circle", caller("circle"))

        # provide the task as an argument
        self.assertEqual("Square", caller("square"))

    def test_050_multiple_plugins(self):
        """Should be available after specifying the plugin name and task name"""
        caller = self.get_caller([multiple_methods.Shape, single_method.Person])

        # without arguments, can not determine the task to run
        with self.assertRaisesRegex(AssertionError, "The parser did not find a task"):
            caller()

        # provide the plugin as an argument (task name is not needed, as Person only has one task)
        self.assertEqual("I have very little to say.", caller("person"))

        # provide the plugin and task as an argument
        self.assertEqual("Circle", caller("shape", "circle"))

        # provide the plugin and task as an argument
        self.assertEqual("Square", caller("shape", "square"))

    def test_060_naming_convention(self):
        """Should convert Plugin name, task name, and argument name to conform with naming conventions"""
        caller = self.get_caller([naming_convention.This_was__a_weirdMIXTure__, naming_convention.ThisWasCamelCase])
        self.assertEqual("this-was-a-weird-mixture", caller("this-was-a-weird-mixture"))
        self.assertEqual("this-was-camel-case", caller("this-was-camel-case", "expected-class-name"))
        self.assertEqual("this-was-underscored", caller("this-was-camel-case", "this-was-underscored"))
        self.assertEqual("this-was-camel-case", caller("this-was-camel-case", "this-was-camel-case"))
        self.assertEqual("this-was-also-underscored", caller("this-was-camel-case", "this-was-also-underscored"))
        self.assertEqual(("a", "b", "c", "d"), caller("this-was-camel-case", "required-arguments", "a", "b", "c", "d"))
        self.assertEqual(("A", "B", "C", "D"), caller("this-was-camel-case", "optional-arguments"))

    def test_070_string_type_annotation(self):
        """Should understand string type annotation"""
        caller = self.get_caller([type_annotation.TypeAnnotation])
        self.assertEqual("Hello World", caller("required-string", "Hello World"))
        self.assertEqual("Alternative", caller("optional-string", "--string=Alternative"))
        self.assertEqual("Hello World!", caller("optional-string"))

    def test_080_boolean_type_annotation(self):
        """Should understand boolean type annotation"""
        caller = self.get_caller([type_annotation.TypeAnnotation])
        self.assertTrue(caller("required-boolean", "--check"))
        self.assertFalse(caller("required-boolean", "--no-check"))
        self.assertTrue(caller("optional-boolean-true"))
        self.assertFalse(caller("optional-boolean-true", "--no-check"))
        self.assertFalse(caller("optional-boolean-false"))
        self.assertTrue(caller("optional-boolean-false", "--check"))

    def test_090_integer_type_annotation(self):
        """Should understand integer type annotation"""
        caller = self.get_caller([type_annotation.TypeAnnotation])
        self.assertEqual(123, caller("required-integer", "123"))
        self.assertEqual(42, caller("optional-integer"))
        self.assertEqual(123, caller("optional-integer", "--number", "123"))

    def test_100_float_type_annotation(self):
        """Should understand float type annotation"""
        caller = self.get_caller([type_annotation.TypeAnnotation])
        self.assertEqual(0.5, caller("required-float", "0.5"))
        self.assertEqual(3.14, caller("optional-float"))
        self.assertEqual(0.5, caller("optional-float", "--number", "0.5"))

    def test_110_file_type_annotation(self):
        """Should understand file, i.e. open, type annotation"""
        caller = self.get_caller([type_annotation.TypeAnnotation])

        expected = "First line\nSecond line\nThird line"
        self.assertEqual(expected, caller("required-file", os.path.join(os.path.dirname(__file__), "file_type_annotation/input.txt")))
        self.assertEqual(expected, caller("optional-file", "--file", os.path.join(os.path.dirname(__file__), "file_type_annotation/input.txt")))

        expected = "#!/usr/bin/env python3"
        self.assertEqual(
            expected,
            caller("optional-file", "--length", str(len(expected))))

    def test_120_choices_configuration(self):
        """Should accept predefined choices"""
        caller = self.get_caller([task_configuration.ConfigurationPlugin])

        # using available choice
        self.assertTrue(caller("required-choice", "yes"))

        # using unavailable choice
        with self.assertRaises(SystemExit):
            caller("required-choice", "unavailable")
