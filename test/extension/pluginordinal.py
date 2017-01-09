#!/usr/bin/env python3

import yaz

class Ordinal(yaz.Plugin):
    @classmethod
    def yaz_get_ordinal(cls):
        return 8

    @yaz.task
    def stack(self):
        return ["low ({})".format(low.yaz_get_ordinal())] + super().stack()
low = Ordinal

class Ordinal(yaz.Plugin):
    @classmethod
    def yaz_get_ordinal(cls):
        return 1024

    @yaz.task
    def stack(self):
        return ["high ({})".format(high.yaz_get_ordinal())]
high = Ordinal

class Ordinal(yaz.Plugin):
    @yaz.task
    def stack(self):
        return ["default ({})".format(default.yaz_get_ordinal())] + super().stack()
default = Ordinal

class Ordinal(yaz.BasePlugin):
    @yaz.task
    def stack(self):
        return ["base ({})".format(base.yaz_get_ordinal())] + super().stack()
base = Ordinal

class Ordinal(yaz.CustomPlugin):
    @yaz.task
    def stack(self):
        return ["custom ({})".format(custom.yaz_get_ordinal())] + super().stack()
custom = Ordinal

if __name__ == "__main__":
    yaz.main()
