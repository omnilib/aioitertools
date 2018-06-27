# Copyright 2018 John Reese
# Licensed under the MIT license

"""
Async-compatible version of itertools standard library functions.

These functions build on top of the async builtins components,
enabling use of both standard iterables and async iterables, without
needing to use if/else clauses or awkward logic.  Standard iterables
get wrapped in async generators, and all functions are designed for
use with `await`, `async for`, etc.

See https://docs.python.org/3/library/itertools.html for reference.
"""

import asyncio
import operator
from typing import AsyncIterator, Callable

from .builtins import iter, list, next
from .types import AnyIterable, AnyIterableIterable, AnyStop, T

# infinite iterators


async def count(start: int = 0, step: int = 1) -> AsyncIterator[T]:
    value = start
    while True:
        yield value
        value += step


async def cycle(itr: AnyIterable) -> AsyncIterator[T]:
    items = []
    async for item in iter(itr):
        yield item
        items.append(item)

    while True:
        for item in items:
            yield item


async def repeat(elem: T, n: int = -1) -> AsyncIterator[T]:
    while True:
        if n == 0:
            break
        yield elem
        n -= 1


# iterators terminating on shortest input sequence


async def accumulate(
    itr: AnyIterable, func: Callable[[T], T] = operator.add
) -> AsyncIterator[T]:
    itr = iter(itr)
    try:
        total: T = await next(itr)
    except AnyStop:
        return

    yield total
    if asyncio.iscoroutinefunction(func):
        async for item in itr:
            total = await func(total, item)
            yield total
    else:
        async for item in itr:
            total = func(total, item)
            yield total


async def chain(*itrs: AnyIterable) -> AsyncIterator[T]:
    async for itr in iter(itrs):
        async for item in iter(itr):
            yield item


def chain_from_iterable(itrs: AnyIterableIterable) -> AsyncIterator[T]:
    return chain(*itrs)


chain.from_iterable = chain_from_iterable
