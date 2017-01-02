#!/usr/bin/env python3

from yaz.task import task
from yaz.main import main
from yaz.plugin import Plugin

class Food(Plugin):
    class Flavors(Plugin):
        @task
        def bitter(self):
            pass

        @task
        def sweet(self):
            pass

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

class Empty(Plugin):
    """Plugin without tasks"""
    pass

if __name__ == "__main__":
    main()
