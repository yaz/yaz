#!/usr/bin/env python3

# in the context of nosetests `import yaz` is not available
try:
    from yaz import yaz
except ImportError:
    import yaz

class Ordinal(yaz.Plugin):
    @classmethod
    def get_yaz_plugin_ordinal(cls):
        return 8

    @yaz.task
    def stack(self):
        return ["low ({})".format(low.get_yaz_plugin_ordinal())] + super().stack()
low = Ordinal

class Ordinal(yaz.Plugin):
    @classmethod
    def get_yaz_plugin_ordinal(cls):
        return 1024

    @yaz.task
    def stack(self):
        return ["high ({})".format(high.get_yaz_plugin_ordinal())]
high = Ordinal

class Ordinal(yaz.Plugin):
    @yaz.task
    def stack(self):
        return ["default ({})".format(default.get_yaz_plugin_ordinal())] + super().stack()
default = Ordinal

if __name__ == "__main__":
    yaz.main()
