#!/usr/bin/env python3

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
        return file.read(length)

    @yaz.task
    def optional_file(self, file: open = __file__, length: int = 1024):
        return file.read(length)


if __name__ == "__main__":
    yaz.main()
