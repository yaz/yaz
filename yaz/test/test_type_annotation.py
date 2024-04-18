#!/usr/bin/env python3

import os
import yaz


class TypeAnnotation(yaz.Plugin):
    @yaz.task
    def required_boolean(self, check: bool):
        return check

    @yaz.task
    def optional_boolean_true(self, check: bool = True):
        return check

    @yaz.task
    def optional_boolean_false(self, check: bool = False):
        return check

    @yaz.task
    def required_integer(self, number: int):
        return number

    @yaz.task
    def optional_integer(self, number: int = 42):
        return number

    @yaz.task
    def required_float(self, number: float):
        return number

    @yaz.task
    def optional_float(self, number: float = 3.14):
        return number

    @yaz.task
    def required_string(self, string: str):
        return string

    @yaz.task
    def optional_string(self, string: str = "Hello World!"):
        return string

    @yaz.task
    def required_file(self, file: open, length: int = 1024):
        try:
            return file.read(length)
        finally:
            file.close()

    @yaz.task
    def optional_file(self, file: open = __file__, length: int = 1024):
        try:
            return file.read(length)
        finally:
            file.close()

    @yaz.task
    def required_literal(self, option: Literal["Yes", 42, 3.14]):
        return option

    @yaz.task
    def optional_literal(self, option: Literal["Yes", 42, 3.14] = "Yes"):
        return option


class Test(yaz.TestCase):
    def test_010_string_type_annotation(self):
        """Should understand string type annotation"""
        caller = self.get_caller([TypeAnnotation])
        self.assertEqual("Hello World", caller("required-string", "Hello World"))
        self.assertEqual("Alternative", caller("optional-string", "--string=Alternative"))
        self.assertEqual("Hello World!", caller("optional-string"))

    def test_020_boolean_type_annotation(self):
        """Should understand boolean type annotation"""
        caller = self.get_caller([TypeAnnotation])
        self.assertTrue(caller("required-boolean", "--check"))
        self.assertFalse(caller("required-boolean", "--no-check"))
        self.assertTrue(caller("optional-boolean-true"))
        self.assertTrue(caller("optional-boolean-true", "--check"))
        self.assertFalse(caller("optional-boolean-true", "--no-check"))
        self.assertFalse(caller("optional-boolean-false"))
        self.assertFalse(caller("optional-boolean-false", "--no-check"))
        self.assertTrue(caller("optional-boolean-false", "--check"))

    def test_030_integer_type_annotation(self):
        """Should understand integer type annotation"""
        caller = self.get_caller([TypeAnnotation])
        self.assertEqual(123, caller("required-integer", "123"))
        self.assertEqual(42, caller("optional-integer"))
        self.assertEqual(123, caller("optional-integer", "--number", "123"))

    def test_040_float_type_annotation(self):
        """Should understand float type annotation"""
        caller = self.get_caller([TypeAnnotation])
        self.assertEqual(0.5, caller("required-float", "0.5"))
        self.assertEqual(3.14, caller("optional-float"))
        self.assertEqual(0.5, caller("optional-float", "--number", "0.5"))

    def test_050_file_type_annotation(self):
        """Should understand file, i.e. open, type annotation"""
        caller = self.get_caller([TypeAnnotation])
        expected = "First line\nSecond line\nThird line"
        self.assertEqual(expected, caller("required-file", os.path.join(os.path.dirname(__file__), "file_type_annotation/input.txt")))
        self.assertEqual(expected, caller("optional-file", "--file", os.path.join(os.path.dirname(__file__), "file_type_annotation/input.txt")))
        with open(__file__) as file:
            self.assertEqual(file.read(128), caller("optional-file", "--length", "128"))

    def test_060_literal_type_annotation(self):
        """Should understand string, integer, and float Literal type annotation"""
        caller = self.get_caller([TypeAnnotation])
        self.assertEqual("Yes", caller("required-literal", "Yes"))
        self.assertEqual(42, caller("required-literal", "42"))
        self.assertEqual(3.14, caller("required-literal", "3.14"))
        # todo: add optional-literal


if __name__ == "__main__":
    yaz.main()
