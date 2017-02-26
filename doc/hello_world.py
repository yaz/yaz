#!/usr/bin/env python3
# file: hello_world.py

import yaz


@yaz.task
def say(message="Hello World!"):
    return message


if __name__ == "__main__":
    yaz.main()
