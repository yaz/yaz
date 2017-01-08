#!/usr/bin/env python3

# in the context of nosetests `import yaz` is not available
try:
    from yaz import yaz
except ImportError:
    import yaz

@yaz.task
def foo():
    return "Foo"

@yaz.task
def bar():
    return "Bar"

if __name__ == "__main__":
    yaz.main()
