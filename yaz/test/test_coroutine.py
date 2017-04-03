#!/usr/bin/env python3

import asyncio
import yaz


class Coroutine(yaz.Plugin):
    @yaz.task
    async def do_one(self, sleep: float):
        await asyncio.sleep(sleep)
        return sleep

    @yaz.task
    async def do_many(self, count: int, sleep: float):
        return await asyncio.gather(*[self.do_one(sleep) for _ in range(count)])


class TestTask(yaz.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.caller = self.get_caller([Coroutine])
        self.loop = asyncio.get_event_loop()
        self.sleep = 0.1
        self.delta = self.sleep * 0.25

    def test_010_one(self):
        """Should call one task asynchronously"""
        start = self.loop.time()
        self.assertEqual(self.sleep, self.caller("do-one", str(self.sleep)))
        self.assertAlmostEqual(self.sleep, self.loop.time() - start, delta=self.delta)

    def test_020_many(self):
        """Should call multiple tasks asynchronously"""
        start = self.loop.time()
        self.assertEqual([self.sleep for _ in range(10)], self.caller("do-many", "10", str(self.sleep)))
        self.assertAlmostEqual(self.sleep, self.loop.time() - start, delta=self.delta)


if __name__ == "__main__":
    yaz.main()
