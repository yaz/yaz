#!/usr/bin/env python3

import yaz


class DependencyInjectionFoodHelper(yaz.Plugin):
    def output(self, message, shout):
        if shout:
            return message.upper()
        else:
            return message


class DependencyInjectionFood(yaz.Plugin):
    @yaz.dependency
    def set_helper(self, helper: DependencyInjectionFoodHelper):
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


class DependencyInjectionMoreFood(yaz.Plugin):
    @yaz.dependency
    def set_helper(self, helper: DependencyInjectionFoodHelper):
        self.helper = helper

    @yaz.task
    def get_helper(self):
        return self.helper

    @yaz.task
    def dummy(self):
        pass


class Test(yaz.TestCase):
    def test_010_dependency_injection(self):
        """Should call dependency setter"""
        food = yaz.get_plugin_instance(DependencyInjectionFood)
        self.assertEqual("Breakfast is ready", food.breakfast())
        self.assertEqual("BREAKFAST IS READY", food.breakfast(shout=True))

    def test_020_singleton_dependency_injection(self):
        """Should inject the same dependency for different dependent plugins"""
        food = yaz.get_plugin_instance(DependencyInjectionFood)
        more_food = yaz.get_plugin_instance(DependencyInjectionMoreFood)
        self.assertEqual(food.get_helper(), more_food.get_helper())


if __name__ == "__main__":
    yaz.main()
