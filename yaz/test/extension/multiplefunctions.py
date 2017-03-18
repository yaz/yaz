#!/usr/bin/env python3

import yaz


@yaz.task
def foo():
    """Well... why not "foo"?"""
    return "Foo"


@yaz.task
def bar():
    '''I disagree and subsequently prefer "bar"'''
    return "Bar"


@yaz.task
def moo_milk():
    """Print something "cow" related"""
    return "Moo Milk"


if __name__ == "__main__":
    yaz.main()
