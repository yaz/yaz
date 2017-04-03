#!/usr/bin/env python3

import yaz


class MultipleMethodsOne(yaz.Plugin):
    @yaz.task
    def talk(self):
        return "I have very little to say."


class MultipleMethodsTwo(yaz.Plugin):
    @yaz.task
    def circle(self):
        return "Circle"

    @yaz.task
    def square(self):
        return "Square"


class Test(yaz.TestCase):
    def test_010_multiple_methods(self):
        """When a single plugin with multiple methods is available, then this should be called without needing to specify the plugin name"""
        caller = self.get_caller([MultipleMethodsTwo])

        # without arguments, can not determine the task to run
        with self.assertRaisesRegex(AssertionError, "The parser did not find a task"):
            caller()

        # provide the task as an argument
        self.assertEqual("Circle", caller("circle"))

        # provide the task as an argument
        self.assertEqual("Square", caller("square"))

    def test_020_multiple_plugins(self):
        """When multiple plugins with multiple methods are available, then this should be called using both the plugin and task name"""
        caller = self.get_caller([MultipleMethodsOne, MultipleMethodsTwo])

        # without arguments, can not determine the task to run
        with self.assertRaisesRegex(AssertionError, "The parser did not find a task"):
            caller()

        # provide the plugin as an argument (task name is not needed, as Person only has one task)
        self.assertEqual("I have very little to say.", caller("multiple-methods-one"))

        # provide the plugin and task as an argument
        self.assertEqual("Circle", caller("multiple-methods-two", "circle"))

        # provide the plugin and task as an argument
        self.assertEqual("Square", caller("multiple-methods-two", "square"))


if __name__ == "__main__":
    yaz.main()
