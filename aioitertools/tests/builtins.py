# Copyright 2018 John Reese
# Licensed under the MIT license

import asyncio
from typing import AsyncIterator
from unittest import TestCase

import aioitertools as ait

from .helpers import async_test

slist = ["A", "B", "C"]
srange = range(3)


class BuiltinsTest(TestCase):

    # aioitertools.iter()

    @async_test
    async def test_iter_list(self):
        it = ait.iter(slist)
        self.assertIsInstance(it, AsyncIterator)
        idx = 0
        async for item in it:
            self.assertEqual(item, slist[idx])
            idx += 1

    @async_test
    async def test_iter_range(self):
        it = ait.iter(srange)
        self.assertIsInstance(it, AsyncIterator)
        idx = 0
        async for item in it:
            self.assertEqual(item, srange[idx])
            idx += 1

    @async_test
    async def test_iter_iterable(self):
        sentinel = object()

        class async_iterable:
            def __aiter__(self):
                return sentinel

        aiter = async_iterable()
        self.assertEqual(ait.iter(aiter), sentinel)

    @async_test
    async def test_iter_iterator(self):
        sentinel = object()

        class async_iterator:
            def __aiter__(self):
                return sentinel

            def __anext__(self):
                return sentinel

        aiter = async_iterator()
        self.assertEqual(ait.iter(aiter), aiter)

    @async_test
    async def test_iter_async_generator(self):
        async def async_gen():
            yield 1
            yield 2

        agen = async_gen()
        self.assertEqual(ait.iter(agen), agen)

    # aioitertools.next()

    @async_test
    async def test_next_list(self):
        it = ait.iter(slist)
        self.assertEqual(await ait.next(it), "A")
        self.assertEqual(await ait.next(it), "B")
        self.assertEqual(await ait.next(it), "C")
        with self.assertRaises(StopAsyncIteration):
            await ait.next(it)

    @async_test
    async def test_next_range(self):
        it = ait.iter(srange)
        self.assertEqual(await ait.next(it), 0)
        self.assertEqual(await ait.next(it), 1)
        self.assertEqual(await ait.next(it), 2)
        with self.assertRaises(StopAsyncIteration):
            await ait.next(it)

    @async_test
    async def test_next_iterable(self):
        class async_iter:
            def __init__(self):
                self.index = 0

            def __aiter__(self):
                return self

            def __anext__(self):
                if self.index > 2:
                    raise StopAsyncIteration()
                return self.next()

            async def next(self):
                value = slist[self.index]
                self.index += 1
                return value

        it = ait.iter(async_iter())
        self.assertEqual(await ait.next(it), "A")
        self.assertEqual(await ait.next(it), "B")
        self.assertEqual(await ait.next(it), "C")
        with self.assertRaises(StopAsyncIteration):
            await ait.next(it)

    @async_test
    async def test_next_async_generator(self):
        async def async_gen():
            for item in slist:
                yield item

        it = ait.iter(async_gen())
        self.assertEqual(await ait.next(it), "A")
        self.assertEqual(await ait.next(it), "B")
        self.assertEqual(await ait.next(it), "C")
        with self.assertRaises(StopAsyncIteration):
            await ait.next(it)

    # aioitertools.list()

    @async_test
    async def test_list(self):
        self.assertEqual(await ait.list(ait.iter(slist)), slist)

    # aioitertools.set()

    @async_test
    async def test_set(self):
        self.assertEqual(await ait.set(ait.iter(slist)), set(slist))

    # aioitertools.enumerate()

    @async_test
    async def test_enumerate(self):
        async for index, value in ait.enumerate(slist):
            self.assertEqual(value, slist[index])

    @async_test
    async def test_enumerate_start(self):
        async for index, value in ait.enumerate(slist, 4):
            self.assertEqual(value, slist[index - 4])

    # aioitertools.map()

    @async_test
    async def test_map_function_list(self):
        idx = 0
        async for value in ait.map(str.lower, slist):
            self.assertEqual(value, slist[idx].lower())
            idx += 1

    @async_test
    async def test_map_function_async_generator(self):
        async def gen():
            for item in slist:
                yield item

        idx = 0
        async for value in ait.map(str.lower, gen()):
            self.assertEqual(value, slist[idx].lower())
            idx += 1

    @async_test
    async def test_map_coroutine_list(self):
        async def double(x):
            await asyncio.sleep(0.0001)
            return x * 2

        idx = 0
        async for value in ait.map(double, slist):
            self.assertEqual(value, slist[idx] * 2)
            idx += 1

    @async_test
    async def test_map_coroutine_generator(self):
        async def gen():
            for item in slist:
                yield item

        async def double(x):
            await asyncio.sleep(0.0001)
            return x * 2

        idx = 0
        async for value in ait.map(double, gen()):
            self.assertEqual(value, slist[idx] * 2)
            idx += 1

    # aioitertools.sum()

    @async_test
    async def test_sum_range_default(self):
        self.assertEqual(await ait.sum(srange), sum(srange))

    @async_test
    async def test_sum_list_string(self):
        self.assertEqual(await ait.sum(slist, "foo"), "fooABC")

    # aioitertools.zip()

    @async_test
    async def test_zip_equal(self):
        idx = 0
        async for a, b in ait.zip(slist, srange):
            self.assertEqual(a, slist[idx])
            self.assertEqual(b, srange[idx])
            idx += 1
