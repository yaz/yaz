#!/usr/bin/env python3

# in the context of nosetests `import yaz` is not available
from yaz import yaz

class TypeAnnotation(yaz.Plugin):
    @yaz.task
    def required_boolean(self, check:bool):
        return check

    @yaz.task
    def optional_boolean_true(self, check:bool=True):
        return check

    @yaz.task
    def optional_boolean_false(self, check:bool=False):
        return check

    @yaz.task
    def required_integer(self, number:int):
        return number

    @yaz.task
    def optional_integer(self, number:int=42):
        return number

    @yaz.task
    def required_float(self, number:float):
        return number

    @yaz.task
    def optional_float(self, number:float=3.14):
        return number

if __name__ == "__main__":
    yaz.main()
