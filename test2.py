#!/usr/bin/env python3

from yaz.task import task
from yaz.main import main

@task
def foo(message="Hello"):
    return "FOO: {}".format(message)

@task
def bar(message):
    return "BAR: {}".format(message)

@task
def get_string(message:str="Hello World"):
    return message

@task
def get_optional_bool(message:bool=True):
    return message

@task
def get_required_bool(message:bool):
    return message

if __name__ == "__main__":
    main()
