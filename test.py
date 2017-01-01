#!/usr/bin/env python3

from yaz.task import task
from yaz.main import main

@task
def say(message="Hello World!"):
    return "SAY: {}".format(message)

if __name__ == "__main__":
    main()
