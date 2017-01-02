#!/usr/bin/env python3

from yaz.task import task
from yaz.main import main
from yaz.plugin import Plugin
from yaz_scripting_plugin import Scripting

class Food(Plugin):
    def __init__(self, scripting:Scripting):
        self.scripting = scripting

    @task
    def ls(self, message="Yes please"):
        return self.scripting.call("ls -la")

if __name__ == "__main__":
    main()
