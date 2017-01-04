#!/usr/bin/env python3

import asyncio

from yaz.task import task
from yaz.main import main
from yaz.plugin import Plugin

class Main(Plugin):
    async def compute(self, sleep):
        await asyncio.sleep(sleep)
        return sleep

    @task
    async def main(self, message="Yes please"):
        return await asyncio.gather(self.compute(0.5), self.compute(1.0), self.compute(0.5))

if __name__ == "__main__":
    main()
