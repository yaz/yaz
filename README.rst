===================
YAZ (Yet another z)
===================

It's purpose is to easily expose python functions and classes, represented as
tasks and plugins, on your console command line.

Yaz is inspired by ``z``, a scripting tool used by Zicht Online.

Features include:

- expose python functions using ``@yaz.task``
- expose type aware function parameters (string, integer, float, boolean, file, etc)
- group tasks together by extending ``yaz.Plugin`` (nested classes provide further grouping)
- handling dependencies between plugins using ``@yaz.dependency``
- asyncio aware


Installing
----------

    .. code-block:: bash

        pip3 install --upgrade yaz


Expose a single function (task)
-------------------------------

The simplest usage of ``yaz`` is to expose a python function to be
executed from the shell.  For example, when you want to run the file
``hello_world.py`` from shell, you could use the following python code:

    .. code-block:: python

        #!/usr/bin/env python3
        # file: examples/01_say.py

        import yaz

        @yaz.task
        def say(message="Hello World!"):
            return message

        if __name__ == "__main__":
            yaz.main()

The above can be called using ``./examples/01_say.py --help``, resulting in a list
of options.  The ``message`` parameter is optional, just like it is in
the python code.  For example:

    .. code-block::

        usage: say.py [-h] [--message MESSAGE]

        optional arguments:
          -h, --help         show this help message and exit
          --message MESSAGE  defaults to message='Hello World!'

When multiple functions are decorated with ``@yaz.task``, all these functions
will be exposed to the console.  This means that the desired function will
need to be specified when the script is run.


Expose functions in a class (plugin with tasks)
-----------------------------------------------

It is common to group functions, with the same subject, together in a class.
Such a class must extend the ``yaz.Plugin`` class to allow, amongst other things,
for class initialization when the task is executed.

Furthermore, classes can have dependencies on each other which will be
resolved by ``yaz``.  This is shown in the example below with ``@yaz.dependency``.

    .. code-block:: python

        #!/usr/bin/env python3
        # file: examples/02_food.py

        import yaz


        class Helper(yaz.Plugin):
            def output(self, message, shout):
                if shout:
                    print(message.upper())
                else:
                    print(message)


        class Food(yaz.Plugin):
            @yaz.dependency
            def set_helper(self, helper: Helper):
                self.helper = helper

            @yaz.task
            def breakfast(self, message="Breakfast is ready", shout: bool = False):
                """Say something in the morning"""
                self.helper.output(message, shout)

            @yaz.task
            def lunch(self, message="Time for lunch", shout: bool = False):
                """Say something in the afternoon"""
                self.helper.output(message, shout)

            @yaz.task
            def dinner(self, message="Dinner is served", shout: bool = False):
                """Say something in the evening"""
                self.helper.output(message, shout)


        if __name__ == "__main__":
            yaz.main()

The above can be called using ``./examples/02_food.py lunch --shout``, resulting in
``DINNER IS SERVED``.  This is achieved using the following steps:

1. When ``yaz.main()`` is called, all the plugins and tasks are collected,
   and it is determined that the ``def lunch(...)`` function is to be called.
2. The ``Food`` class is initiated.
3. The dependencies for the ``Food`` class are resolved, i.e. the ``Helper``
   class is initiated and ``def set_helper`` is called.
4. The ``lunch`` method is called and ``yaz.main()`` prints its return value.


TODO
----

- todo: explain multiple plugins
- todo: explain different argument types
- todo: explain @yaz.task(OPTIONS)
- todo: explain plugin inheritance
- todo: explain coroutines / asyncio
- todo: explain available base plugins: yaz_templating_plugin and yaz_scripting_plugin

Maintainer(s)
-------------

- Boudewijn Schoon <boudewijn@zicht.nl>
