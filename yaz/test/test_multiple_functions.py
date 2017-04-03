#!/usr/bin/env python3

import yaz


@yaz.task
def multiple_functions_foo():
    """Well... why not "foo"?"""
    return "Foo"


@yaz.task
def multiple_functions_bar():
    '''I disagree and subsequently prefer "bar"'''
    return "Bar"


class Test(yaz.TestCase):
    def test_010(self):
        """When multiple functions are available, then the names of these functions must be given to specify which task to run"""
        caller = self.get_caller([multiple_functions_foo, multiple_functions_bar])

        # without arguments, can not determine the task to run
        with self.assertRaisesRegex(AssertionError, "The parser did not find a task"):
            caller()

        # provide the task as an argument
        self.assertEqual("Foo", caller("multiple-functions-foo"))

        # provide the task as an argument
        self.assertEqual("Bar", caller("multiple-functions-bar"))


if __name__ == "__main__":
    yaz.main()
