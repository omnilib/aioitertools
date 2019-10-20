# Copyright 2018 John Reese
# Licensed under the MIT license

import asyncio
import functools
from unittest import TestCase

from aioitertools.helpers import maybe_await


def async_test(fn):
    def wrapped(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(fn(*args, **kwargs))

    return wrapped


class HelpersTest(TestCase):

    # aioitertools.helpers.maybe_await()

    @async_test
    async def test_maybe_await(self):
        self.assertEqual(await maybe_await(42), 42)

    @async_test
    async def test_maybe_await_async_def(self):
        async def forty_two():
            await asyncio.sleep(0.0001)
            return 42

        self.assertEqual(await maybe_await(forty_two()), 42)

    @async_test
    async def test_maybe_await_coroutine(self):
        @asyncio.coroutine
        def forty_two():
            yield from asyncio.sleep(0.0001)
            return 42

        self.assertEqual(await maybe_await(forty_two()), 42)

    @async_test
    async def test_maybe_await_partial(self):
        async def multiply(a, b):
            await asyncio.sleep(0.0001)
            return a * b

        self.assertEqual(await maybe_await(functools.partial(multiply, 6)(7)), 42)
