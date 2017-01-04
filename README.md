# Yet Another Z
`z` is a scripting tool used by Zicht Online.  `yaz` is a python tool
inspired by `z`.

# Installing
From source:
```
git clone git@github.com:boudewijn-zicht/yaz.git
cd yaz
python3 setup.py install
```

From source (for development)
```
git clone git@github.com:boudewijn-zicht/yaz.git
cd yaz
python3 setup.py develop

# run test cases
pip3 install nose
nosetests --with-coverage --cover-package yaz
```

From a package (todo: yaz is not yet a registered package)
```
pip3 install yaz
```

# Expose a single function
The most simplest usage of `yaz` is to expose a python function to be
executed from the shell.  For example, when you want to run the file
`say.py` from shell, you could use the following python code:

```
#!/usr/bin/env python3
# file: say.py

import yaz

@yaz.task
def say(message="Hello World!"):
    return message
    
if __name__ == "__main__":
    yaz.main()
```

The above can be called using `./say.py --help`, resulting in a list
of options.  The `message` parameter is automatically provided as an
optional argument.

# Expose multiple functions
More advanced usage allows multiple tasks to be provided and possibly
grouped together in `Plugin` classes.  These plugins can have
dependencies on other plugins, which will be automatically resolved.

For example, todo

```
#!/usr/bin/env python3
# file: food.py

import yaz

class Helper(yaz.Plugin):
    def output(self, message, shout):
        if shout:
            print(message.upper())
        else:
            print(message)

class Food(yaz.Plugin):
    def __init__(self, helper: Helper):
        self.helper = helper
        
    @yaz.task
    def breakfast(self, message="Breakfast is ready", shout:bool=False):
        self.helper.output(message, shout)
        
    @yaz.task
    def lunch(self, message="Time for lunch", shout:bool=False):
        self.helper.output(message, shout)
        
    @yaz.task
    def dinner(self, message="Dinner is served", shout:bool=False):
        self.helper.output(message, shout)
        
if __name__ == "__main__":
    yaz.main()
```

The above can be called using `./food.py --help`, resulting in a list
of actions, i.e. `breakfast`, `lunch`, and `dinner`.  Each have the
options `message` and `shout`.  Note that `shout` is defined as a
boolean, and hence provided as a `--shout` flag insead of `message`,
which is available as `--message "alternative message"`.

todo: explain multiple plugins
todo: explain different arguments
todo: explain @yaz.task(OPTIONS)
todo: explain plugin inherritance
todo: explain coroutines
todo: explain available base plugins: yaz_templating_plugin and yaz_scripting_plugin
