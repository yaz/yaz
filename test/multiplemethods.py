#!/usr/bin/env python3

# in the context of nosetests `import yaz` is not available
from yaz import yaz

class Shape(yaz.Plugin):
    @yaz.task
    def circle(self):
        return "Circle"

    @yaz.task
    def square(self):
        return "Square"

if __name__ == "__main__":
    yaz.main()
