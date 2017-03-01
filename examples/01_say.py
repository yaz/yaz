#!/usr/bin/env python3

"""
An example of a script that only contains a single yaz task.

Because there is only a single task, there is no need to specify
which task is to be run when calling this script.  For example:


$ ./01_say.py
usage: hello_world.py [-h] [--message MESSAGE]

Print MESSAGE to the console

optional arguments:
  -h, --help         show this help message and exit
  --message MESSAGE  defaults to message='Hello World!'


$ ./01_say.py
Hello World!


$ ./01_say.py --message "Alternative message"
Alternative message
"""

import yaz


@yaz.task
def say(message: str = "Hello World!"):
    """Print MESSAGE to the console"""
    return message


if __name__ == "__main__":
    yaz.main()
