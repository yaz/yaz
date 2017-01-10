#!/usr/bin/env python3

from yaz.task import task
from yaz.main import main
from yaz.plugin import Plugin


class Main(Plugin):
    @task
    def main(self, message="Yes please"):
        return message


if __name__ == "__main__":
    main()
