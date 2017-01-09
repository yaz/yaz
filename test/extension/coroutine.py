#!/usr/bin/env python3

import asyncio

import yaz

class Coroutine(yaz.Plugin):
    @yaz.task
    async def do_one(self, sleep:float):
        await asyncio.sleep(sleep)
        return sleep

    @yaz.task
    async def do_many(self, count:int, sleep:float):
        return await asyncio.gather(*[self.do_one(sleep) for _ in range(count)])

if __name__ == "__main__":
    yaz.main()
