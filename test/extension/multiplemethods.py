#!/usr/bin/env python3

import yaz

class Shape(yaz.Plugin):
    @yaz.task
    def circle(self):
        return "Circle"

    @yaz.task
    def square(self):
        return "Square"

if __name__ == "__main__":
    yaz.main()
