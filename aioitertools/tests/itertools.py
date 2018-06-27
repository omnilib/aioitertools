# Copyright 2018 John Reese
# Licensed under the MIT license

from unittest import TestCase

import aioitertools as ait
from .helpers import async_test

slist = ["A", "B", "C"]


class ItertoolsTest(TestCase):
    @async_test
    async def test_count_bare(self):
        counter = ait.count()
        self.assertEqual(await ait.next(counter), 0)
        self.assertEqual(await ait.next(counter), 1)
        self.assertEqual(await ait.next(counter), 2)
        self.assertEqual(await ait.next(counter), 3)

    @async_test
    async def test_count_start(self):
        counter = ait.count(42)
        self.assertEqual(await ait.next(counter), 42)
        self.assertEqual(await ait.next(counter), 43)
        self.assertEqual(await ait.next(counter), 44)
        self.assertEqual(await ait.next(counter), 45)

    @async_test
    async def test_count_start_step(self):
        counter = ait.count(42, 3)
        self.assertEqual(await ait.next(counter), 42)
        self.assertEqual(await ait.next(counter), 45)
        self.assertEqual(await ait.next(counter), 48)
        self.assertEqual(await ait.next(counter), 51)

    @async_test
    async def test_count_negative(self):
        counter = ait.count(step=-2)
        self.assertEqual(await ait.next(counter), 0)
        self.assertEqual(await ait.next(counter), -2)
        self.assertEqual(await ait.next(counter), -4)
        self.assertEqual(await ait.next(counter), -6)

    @async_test
    async def test_cycle_list(self):
        it = ait.cycle(slist)
        self.assertEqual(await ait.next(it), "A")
        self.assertEqual(await ait.next(it), "B")
        self.assertEqual(await ait.next(it), "C")
        self.assertEqual(await ait.next(it), "A")
        self.assertEqual(await ait.next(it), "B")
        self.assertEqual(await ait.next(it), "C")
        self.assertEqual(await ait.next(it), "A")

    @async_test
    async def test_cycle_gen(self):
        async def gen():
            yield 1
            yield 2
            yield 42

        it = ait.cycle(gen())
        self.assertEqual(await ait.next(it), 1)
        self.assertEqual(await ait.next(it), 2)
        self.assertEqual(await ait.next(it), 42)
        self.assertEqual(await ait.next(it), 1)
        self.assertEqual(await ait.next(it), 2)
        self.assertEqual(await ait.next(it), 42)
        self.assertEqual(await ait.next(it), 1)

    @async_test
    async def test_repeat(self):
        it = ait.repeat(42)
        self.assertEqual(await ait.next(it), 42)
        self.assertEqual(await ait.next(it), 42)
        self.assertEqual(await ait.next(it), 42)
        self.assertEqual(await ait.next(it), 42)
        self.assertEqual(await ait.next(it), 42)
        self.assertEqual(await ait.next(it), 42)

    @async_test
    async def test_repeat_limit(self):
        it = ait.repeat(42, 5)
        self.assertEqual(await ait.next(it), 42)
        self.assertEqual(await ait.next(it), 42)
        self.assertEqual(await ait.next(it), 42)
        self.assertEqual(await ait.next(it), 42)
        self.assertEqual(await ait.next(it), 42)
        with self.assertRaises(StopAsyncIteration):
            await ait.next(it)
