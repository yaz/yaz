#!/usr/bin/env python3

import yaz


class Person(yaz.Plugin):
    @yaz.task
    def talk(self):
        return "I have very little to say."


if __name__ == "__main__":
    yaz.main()
