#!/usr/bin/env python3

import yaz


class FoodHelper(yaz.Plugin):
    def output(self, message, shout):
        if shout:
            return message.upper()
        else:
            return message


class Food(yaz.Plugin):
    def __init__(self, helper: FoodHelper):
        self.helper = helper

    @yaz.task
    def get_helper(self):
        return self.helper

    @yaz.task
    def breakfast(self, message="Breakfast is ready", shout: bool = False):
        return self.helper.output(message, shout)

    @yaz.task
    def lunch(self, message="Time for lunch", shout: bool = False):
        return self.helper.output(message, shout)

    @yaz.task
    def dinner(self, message="Dinner is served", shout: bool = False):
        return self.helper.output(message, shout)


class MoreFood(yaz.Plugin):
    def __init__(self, helper: FoodHelper):
        self.helper = helper

    @yaz.task
    def get_helper(self):
        return self.helper

    @yaz.task
    def dummy(self):
        pass


if __name__ == "__main__":
    yaz.main()
