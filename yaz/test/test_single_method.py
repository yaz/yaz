#!/usr/bin/env python3

import yaz


class SingleMethod(yaz.Plugin):
    @yaz.task
    def talk(self):
        return "I have very little to say."


class Test(yaz.TestCase):
    def test_010(self):
        """When only a single plugin with only a single method is available, then this should be called without needing to specify the plugin or task name"""
        caller = self.get_caller([SingleMethod])
        self.assertEqual("I have very little to say.", caller())


if __name__ == "__main__":
    yaz.main()
