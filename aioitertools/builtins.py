# Copyright 2018 John Reese
# Licensed under the MIT license

"""
Async-compatible versions of builtin functions for iterables.

These functions intentionally shadow their builtins counterparts,
enabling use with both standard iterables and async iterables, without
needing to use if/else clauses or awkward logic.  Standard iterables
get wrapped in async generators, and all functions are designed for
use with `await`, `async for`, etc.
"""

import asyncio
import builtins
from typing import (
    AsyncIterable,
    AsyncIterator,
    Callable,
    Iterable,
    List,
    Set,
    Tuple,
    Sequence,
    cast,
)

from .types import AnyIterable, AnyIterator, AnyStop, T, R


def iter(itr: AnyIterable) -> AsyncIterator[T]:
    """
    Get an async iterator from any mixed iterable.

    Async iterators will be returned directly.
    Async iterables will return an async iterator.
    Standard iterables will be wrapped in an async generator yielding
    each item in the iterable in the same order.

    Examples:

        async for iter(range(10)):
            ...

    """
    if isinstance(itr, AsyncIterator):
        return itr

    elif isinstance(itr, AsyncIterable):
        return itr.__aiter__()

    async def gen() -> AsyncIterator[T]:
        nonlocal itr
        itr = cast(Iterable[T], itr)
        for item in itr:
            yield item

    return gen()


async def next(itr: AnyIterator) -> T:
    """
    Return the next item of any mixed iterator.

    Calls builtins.next() on standard iterators, and awaits itr.__anext__()
    on async iterators.

    Example:

        value = await next(it)

    """
    if isinstance(itr, AsyncIterator):
        return await itr.__anext__()
    return builtins.next(itr)


async def list(itr: AnyIterable) -> List[T]:
    """
    Consume a mixed iterable and return a list of items in order.

    Example:

        await list(range(5))
        -> [0, 1, 2, 3, 4]

    """
    return [item async for item in iter(itr)]


async def set(itr: AnyIterable) -> Set[T]:
    """
    Consume a mixed iterable and return a set of items.

    Example:

        await set([0, 1, 2, 3, 0, 1, 2, 3])
        -> {0, 1, 2, 3}

    """
    return {item async for item in iter(itr)}


async def enumerate(itr: AnyIterable) -> AsyncIterator[Tuple[int, T]]:
    """
    Consume a mixed iterable and yield the current index and item.

    Example:

        async for index, value in enumerate(...):
            ...

    """
    index = 0
    async for item in iter(itr):
        yield index, item
        index += 1


async def map(fn: Callable[[T], R], itr: AnyIterable) -> AsyncIterator[R]:
    """
    Modify item of a mixed iterable using the given function or coroutine.

    Example:

        async for response in map(func, data):
            ...

    """
    if asyncio.iscoroutinefunction(fn):
        # todo: queue items eagerly
        async for item in iter(itr):
            yield await fn(item)  # type: ignore  # todo: better mixed function type

    else:
        async for item in iter(itr):
            yield fn(item)


async def sum(itr: AnyIterable, start: T = None) -> T:
    """
    Compute the sum of a mixed iterable, adding each value with the start value.

    Example:

        await sum(generator())
        -> 1024

    """
    value: T
    if start is None:
        value = cast(T, 0)  # emulate stdlib but still type nicely for non-ints
    else:
        value = start

    async for item in iter(itr):
        value += item  # type: ignore  # mypy doesn't know T + T

    return value


async def zip(*itrs: AnyIterable) -> AsyncIterator[Sequence[T]]:
    """
    Yield a tuple of items from mixed iterables until the shortest is consumed.

    Example:

        async for a, b, c in zip(i, j, k):
            ...

    """
    its: List[AsyncIterator[T]] = [iter(itr) for itr in itrs]

    while True:
        try:
            values = await asyncio.gather(*[it.__anext__() for it in its])
            yield values
        except AnyStop:
            break
