#!/usr/bin/env python3

"""
An example of a script with a single plugin grouping together
several tasks.

Because there is only a single plugin, there is no need to specify
which plugin is to be run when calling this script.  However, since
there are multiple tasks within the plugin, the tasks do need to be
specified.  For example:


$ ./02_food.py breakfast --help
usage: 02_food.py breakfast [-h] [--message MESSAGE] [--shout]

Say something in the morning

optional arguments:
  -h, --help         show this help message and exit
  --message MESSAGE  defaults to message='Breakfast is ready'
  --shout            defaults to shout=False, pass this flag to set to True


$ ./02_food.py breakfast --shout
BREAKFAST IS READY
"""

import yaz


class Helper(yaz.Plugin):
    def output(self, message, shout):
        if shout:
            return message.upper()
        else:
            return message


class Food(yaz.Plugin):
    """A collection of Food related tasks"""
    @yaz.dependency
    def set_helper(self, helper: Helper):
        self.helper = helper

    @yaz.task
    def breakfast(self, message="Breakfast is ready", shout: bool = False):
        """Say something in the morning"""
        return self.helper.output(message, shout)

    @yaz.task
    def lunch(self, message="Time for lunch", shout: bool = False):
        """Say something in the afternoon"""
        return self.helper.output(message, shout)

    @yaz.task
    def dinner(self, message="Dinner is served", shout: bool = False):
        """Say something in the evening"""
        return self.helper.output(message, shout)


if __name__ == "__main__":
    yaz.main()
