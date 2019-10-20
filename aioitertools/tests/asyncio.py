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

        pairs = [(1, 0.2), (2, 0.1), (3, 0.4), (4, 0.3), (5, 0.15)]
        expected = [2, 5, 1, 4, 3]

        futures = [sleepy(*pair) for pair in pairs]
        results = await ait.list(aio.as_completed(futures))
        self.assertEqual(results, expected)

        futures = [sleepy(*pair) for pair in pairs]
        results = []
        async for value in aio.as_completed(futures):
            results.append(value)
        self.assertEqual(results, expected)
