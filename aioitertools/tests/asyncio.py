# Copyright 2019 John Reese
# Licensed under the MIT license

import asyncio
from unittest import TestCase

import aioitertools as ait
import aioitertools.asyncio as aio
from .helpers import async_test

slist = ["A", "B", "C"]
srange = range(3)


class AsyncioTest(TestCase):
    def test_import(self):
        self.assertEqual(ait.asyncio, aio)

    @async_test
    async def test_as_completed(self):
        async def sleepy(number, duration):
            await asyncio.sleep(duration)
            return number

        pairs = [(1, 0.3), (2, 0.1), (3, 0.5)]
        expected = [2, 1, 3]

        futures = [sleepy(*pair) for pair in pairs]
        results = await ait.list(aio.as_completed(futures))
        self.assertEqual(results, expected)

        futures = [sleepy(*pair) for pair in pairs]
        results = []
        async for value in aio.as_completed(futures):
            results.append(value)
        self.assertEqual(results, expected)

    @async_test
    async def test_as_completed_timeout(self):
        calls = [(1.0,), (0.1,)]

        futures = [asyncio.sleep(*args) for args in calls]
        with self.assertRaises(asyncio.TimeoutError):
            await ait.list(aio.as_completed(futures, timeout=0.5))

        futures = [asyncio.sleep(*args) for args in calls]
        results = 0
        with self.assertRaises(asyncio.TimeoutError):
            async for _ in aio.as_completed(futures, timeout=0.5):
                results += 1
        self.assertEqual(results, 1)

    @async_test
    async def test_gather_input_types(self):
        async def fn(arg):
            await asyncio.sleep(0.001)
            return arg

        fns = [fn(1), asyncio.ensure_future(fn(2))]
        if hasattr(asyncio, "create_task"):
            # 3.7 only
            fns.append(asyncio.create_task(fn(3)))  # pylint: disable=no-member
        else:
            fns.append(fn(3))

        result = await aio.gather(*fns)
        self.assertEqual([1, 2, 3], result)

    @async_test
    async def test_gather_limited(self):
        max_counter = 0
        counter = 0

        async def fn(arg):
            nonlocal counter, max_counter
            counter += 1
            if max_counter < counter:
                max_counter = counter
            await asyncio.sleep(0.001)
            counter -= 1
            return arg

        # Limit of 2
        result = await aio.gather(*[fn(i) for i in range(10)], limit=2)
        self.assertEqual(2, max_counter)
        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], result)

        # No limit
        result = await aio.gather(*[fn(i) for i in range(10)])
        self.assertEqual(
            10, max_counter
        )  # TODO: on a loaded machine this might be less?
        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], result)

    @async_test
    async def test_gather_limited_dupes(self):
        async def fn(arg):
            await asyncio.sleep(0.001)
            return arg

        f = fn(1)
        g = fn(2)
        result = await aio.gather(f, f, f, g, f, g, limit=2)
        self.assertEqual([1, 1, 1, 2, 1, 2], result)

        f = fn(1)
        g = fn(2)
        result = await aio.gather(f, f, f, g, f, g)
        self.assertEqual([1, 1, 1, 2, 1, 2], result)

    @async_test
    async def test_gather_with_exceptions(self):
        class MyException(Exception):
            pass

        async def fn(arg, fail=False):
            await asyncio.sleep(arg)
            if fail:
                raise MyException(arg)
            return arg

        with self.assertRaises(MyException):
            await aio.gather(fn(0.002, fail=True), fn(0.001))

        result = await aio.gather(
            fn(0.002, fail=True), fn(0.001), return_exceptions=True
        )
        self.assertEqual(result[1], 0.001)
        self.assertIsInstance(result[0], MyException)
