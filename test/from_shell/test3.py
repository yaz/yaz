#!/usr/bin/env python3

from yaz.task import task
from yaz.main import main
from yaz.plugin import Plugin


class TestMyNAME(Plugin):
    """Should be accessible as name test-my-name"""

    @task
    def _ignore_first_underscore(self):
        pass

    @task
    def __ignore_first_underscores(self):
        pass

    @task
    def ignore_last_underscore_(self):
        pass

    @task
    def ignore_last_underscores__(self):
        pass

    @task
    def _ignore_underscore_(self):
        pass

    @task
    def __ignore_underscores__(self):
        pass

    @task
    def LOWER_CASE(self):
        pass

    @task
    def FooBar(self):
        pass

    @task
    def fooBar2(self):
        pass


class Dummy(Plugin):
    """Plugin without tasks"""
    pass


class Food(Plugin):
    class Flavors(Plugin):
        @task
        def bitter(self):
            pass

        @task
        def sweet(self):
            pass

    def __init__(self, dummy: Dummy):
        self.dummy = dummy

    @task
    def breakfast(self, message="Yes please"):
        return "FOOD.BREAKFAST: {}".format(message)

    @task
    def lunch(self, message="Yes please"):
        return "FOOD.LUNCH: {}".format(message)

    @task
    def dinner(self, message="Yes please"):
        return "FOOD.DINNER: {}".format(message)

    def i_am_not_a_task(self):
        pass


if __name__ == "__main__":
    main()
