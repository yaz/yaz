#!/usr/bin/env python3
# file: example.py

import yaz


class Helper(yaz.Plugin):
    def output(self, message, shout):
        if shout:
            print(message.upper())
        else:
            print(message)


class Food(yaz.Plugin):
    @yaz.dependency
    def set_helper(self, helper: Helper):
        self.helper = helper

    @yaz.task
    def breakfast(self, message="Breakfast is ready", shout: bool = False):
        self.helper.output(message, shout)

    @yaz.task
    def lunch(self, message="Time for lunch", shout: bool = False):
        self.helper.output(message, shout)

    @yaz.task
    def dinner(self, message="Dinner is served", shout: bool = False):
        self.helper.output(message, shout)


if __name__ == "__main__":
    yaz.main()
