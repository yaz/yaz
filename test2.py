#!/usr/bin/env python3

from yaz.task import task
from yaz.main import main

@task
def foo(message="Hello"):
    return "FOO: {}".format(message)

@task
def bar(message):
    return "BAR: {}".format(message)

if __name__ == "__main__":
    main()
