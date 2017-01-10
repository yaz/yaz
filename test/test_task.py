import sys
import unittest
import asyncio

from yaz.parser import Parser
from yaz.task import get_task_tree

import test.extension.coroutine


class TestTask(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parser = Parser()
        self.parser.add_task_tree(get_task_tree())
        self.loop = asyncio.get_event_loop()
        self.sleep = 0.1
        self.delta = self.sleep * 0.25

    def test_one(self):
        """Should call one task asynchronously"""
        start = self.loop.time()
        task, kwargs = self.parser.parse_arguments([sys.argv[0], "coroutine", "do-one", str(self.sleep)])
        self.assertEqual(self.sleep, task(**kwargs))
        self.assertAlmostEqual(self.sleep, self.loop.time() - start, delta=self.delta)

    def test_many(self):
        """Should call multiple tasks asynchronously"""
        start = self.loop.time()
        task, kwargs = self.parser.parse_arguments([sys.argv[0], "coroutine", "do-many", "10", str(self.sleep)])
        self.assertEqual([self.sleep for _ in range(10)], task(**kwargs))
        self.assertAlmostEqual(self.sleep, self.loop.time() - start, delta=self.delta)
