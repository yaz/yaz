#!/usr/bin/env python3

import yaz


@yaz.task
def single_function_task(message="Hello World!"):
    return message


class Test(yaz.TestCase):
    def test_010(self):
        """When only a single function is available, then this should be called without needing to specify the task name"""
        caller = self.get_caller([single_function_task])

        # without arguments, uses default value for message
        self.assertEqual("Hello World!", caller())

        # provide message value as an argument
        self.assertEqual("I said HELLO!", caller("--message", "I said HELLO!"))


if __name__ == "__main__":
    yaz.main()
