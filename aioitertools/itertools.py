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
import builtins
import itertools
import operator
from typing import Any, AsyncIterator, List, Optional, Sequence, Tuple

from .builtins import enumerate, iter, list, next, zip
from .types import (
    Accumulator,
    AnyFunction,
    AnyIterable,
    AnyIterableIterable,
    AnyStop,
    KeyFunction,
    Predicate,
    R,
    T,
)


async def accumulate(
    itr: AnyIterable, func: Accumulator = operator.add
) -> AsyncIterator[T]:
    """
    Yield the running accumulation of an iterable and operator.

    Accepts both a standard function or a coroutine for accumulation.

    Example:

        data = [1, 2, 3, 4]

        async def mul(a, b):
            return a * b

        async for total in accumulate(data, func=mul):
            ...  # 1, 2, 6, 24

    """
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


class Chain:
    async def __call__(self, *itrs: AnyIterable) -> AsyncIterator[T]:
        """
        Yield values from one or more iterables in series.

        Consumes the first iterable lazily, in entirety, then the second, and so on.

        Example:

            async for value in chain([1, 2, 3], [7, 8, 9]):
                ...  # 1, 2, 3, 7, 8, 9

        """
        async for itr in iter(itrs):
            async for item in iter(itr):
                yield item

    def from_iterable(self, itrs: AnyIterableIterable) -> AsyncIterator[T]:
        """
        Like chain, but takes an iterable of iterables.

        Alias for chain(*itrs)
        """
        return self(*itrs)


chain = Chain()


async def combinations(itr: AnyIterable, r: int) -> AsyncIterator[Sequence[T]]:
    """
    Yield r length subsequences from the given iterable.

    Simple wrapper around itertools.combinations for asyncio.
    This will consume the entire iterable before yielding values.

    Example:

        async for value in combinations(range(4), 3):
            ...  # (0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)

    """
    pool: List[T] = await list(itr)
    for value in itertools.combinations(pool, r):
        yield value


async def combinations_with_replacement(
    itr: AnyIterable, r: int
) -> AsyncIterator[Sequence[T]]:
    """
    Yield r length subsequences from the given iterable with replacement.

    Simple wrapper around itertools.combinations_with_replacement.
    This will consume the entire iterable before yielding values.

    Example:

        async for value in combinations_with_replacement("ABC", 2):
            ...  # ("A", "A"), ("A", "B"), ("A", "C"), ("B", "B"), ...

    """
    pool: List[T] = await list(itr)
    for value in itertools.combinations_with_replacement(pool, r):
        yield value


async def compress(itr: AnyIterable, selectors: AnyIterable) -> AsyncIterator[T]:
    """
    Yield elements only when the corresponding selector evaluates to True.

    Stops when either the iterable or the selectors have been exhausted.

    Example:

        async for value in compress(range(5), [1, 0, 0, 1, 1]):
            ...  # 0, 3, 4
    """
    async for value, selector in zip(itr, selectors):
        if selector:
            yield value


async def count(start: int = 0, step: int = 1) -> AsyncIterator[T]:
    """
    Yield an infinite series, starting at the given value and increasing by step.

    Example:

        async for value in counter(10, -1):
            ...  # 10, 9, 8, 7, ...

    """

    value = start
    while True:
        yield value
        value += step


async def cycle(itr: AnyIterable) -> AsyncIterator[T]:
    """
    Yield a repeating series from the given iterable.

    Lazily consumes the iterable when the next value is needed, and caching
    the values in memory for future iterations of the series.

    Example:

        async for value in cycle([1, 2]):
            ...  # 1, 2, 1, 2, 1, 2, ...

    """
    items = []
    async for item in iter(itr):
        yield item
        items.append(item)

    while True:
        for item in items:
            yield item


async def dropwhile(predicate: Predicate, iterable: AnyIterable) -> AsyncIterator[T]:
    """
    Drops all items until the predicate evaluates False; yields all items afterwards.

    Accepts both standard functions and coroutines for the predicate.

    Example:

        def pred(x):
            return x < 4

        async for item in dropwhile(pred, range(6)):
            ...  # 4, 5, 6

    """
    itr = iter(iterable)
    if asyncio.iscoroutinefunction(predicate):
        async for item in itr:
            if not await predicate(item):
                yield item
                break
    else:
        async for item in itr:
            if not predicate(item):
                yield item
                break
    async for item in itr:
        yield item


async def filterfalse(predicate: Predicate, iterable: AnyIterable) -> AsyncIterator[T]:
    """
    Yield items from the iterable only when the predicate evaluates to False.

    Accepts both standard functions and coroutines for the predicate.

    Example:

        def pred(x):
            return x < 4

        async for item in filterfalse(pred, range(6)):
            ...  # 4, 5

    """
    if asyncio.iscoroutinefunction(predicate):
        async for item in iter(iterable):
            if not await predicate(item):
                yield item
    else:
        async for item in iter(iterable):
            if not predicate(item):
                yield item


async def groupby(
    itr: AnyIterable, key: KeyFunction = None
) -> AsyncIterator[Tuple[Any, Sequence[T]]]:
    """
    Yield consecutive keys and groupings from the given iterable.

    Items will be grouped based on the key function, which defaults to
    the identity of each item.  Accepts both standard functions and
    coroutines for the key function.  Suggest sorting by the key
    function before using groupby.

    Example:

        data = ["A", "a", "b", "c", "C", "c"]

        async for key, group in groupby(data, key=str.lower):
            key  # "a", "b", "c"
            group  # ["A", "a"], ["b"], ["c", "C", "c"]

    """
    if key is None:
        key = lambda x: x

    grouping = []

    it = iter(itr)
    item = await next(it)
    grouping = [item]

    if asyncio.iscoroutinefunction(key):
        j = await key(item)
        async for item in it:
            k = await key(item)
            if k != j:
                yield j, grouping
                grouping = [item]
            else:
                grouping.append(item)
            j = k

    else:
        j = key(item)
        async for item in it:
            k = key(item)
            if k != j:
                yield j, grouping
                grouping = [item]
            else:
                grouping.append(item)
            j = k

    yield j, grouping


async def islice(itr: AnyIterable, *args: int) -> AsyncIterator[T]:
    """
    Yield selected items from the given iterable.

    islice(iterable, stop)
    islice(iterable, start, stop[, step])

    Starting from the start index (or zero), stopping at the stop
    index (or until exhausted), skipping items if step > 0.

    Example:

        data = range(10)

        async for item in islice(data, 5):
            ...  # 0, 1, 2, 3, 4

        async for item in islice(data, 2, 5):
            ...  # 2, 3, 4

        async for item in islice(data, 1, 7, 2):
            ...  # 1, 3, 5

    """
    start = 0
    step = 1
    if not args:
        raise ValueError("must pass stop index")
    elif len(args) == 1:
        stop, = args
    elif len(args) == 2:
        start, stop = args
    elif len(args) == 3:
        start, stop, step = args
    assert start >= 0 and (stop is None or stop >= 0) and step >= 0
    step = max(1, step)

    async for index, item in enumerate(itr):
        if index < start:
            continue
        if stop is not None and index >= stop:
            break
        if (index - start) % step != 0:
            continue
        yield item


async def permutations(itr: AnyIterable, r: int = None) -> AsyncIterator[Sequence[T]]:
    """
    Yield r length permutations of elements in the iterable.

    Simple wrapper around itertools.combinations for asyncio.
    This will consume the entire iterable before yielding values.

    Example:

        async for value in permutations(range(3)):
            ...  # (0, 1, 2), (0, 2, 1), (1, 0, 2), ...

    """
    pool: List[T] = await list(itr)
    for value in itertools.permutations(pool, r):
        yield value


async def product(
    *itrs: AnyIterable, repeat: int = 1  # pylint: disable=redefined-outer-name
) -> AsyncIterator[Sequence[T]]:
    """
    Yield cartesian products of all iterables.

    Simple wrapper around itertools.combinations for asyncio.
    This will consume all iterables before yielding any values.

    Example:

        async for value in product("abc", "xy"):
            ...  # ("a", "x"), ("a", "y"), ("b", "x"), ...

        async for value in product(range(3), repeat=3):
            ...  # (0, 0, 0), (0, 0, 1), (0, 0, 2), ...

    """
    pools = await asyncio.gather(*[list(itr) for itr in itrs])
    for value in itertools.product(*pools, repeat=repeat):
        yield value


async def repeat(elem: T, n: int = -1) -> AsyncIterator[T]:
    """
    Yield the given value repeatedly, forever or up to n times.

    Example:

        async for value in repeat(7):
            ...  # 7, 7, 7, 7, 7, 7, ...

    """
    while True:
        if n == 0:
            break
        yield elem
        n -= 1


async def starmap(fn: AnyFunction, iterable: AnyIterableIterable) -> AsyncIterator[R]:
    """
    Yield values from a function using an iterable of iterables for arguments.

    Each iterable contained within will be unpacked and consumed before
    executing the function or coroutine.

    Example:

        data = [(1, 1), (1, 1, 1), (2, 2)]

        async for value in starmap(operator.add, data):
            ...  # 2, 3, 4

    """
    if asyncio.iscoroutinefunction(fn):
        async for itr in iter(iterable):
            args = await list(itr)
            yield await fn(*args)
    else:
        async for itr in iter(iterable):
            args = await list(itr)
            yield fn(*args)


async def takewhile(predicate: Predicate, iterable: AnyIterable) -> AsyncIterator[T]:
    """
    Yield values from the iterable until the predicate evaluates False.

    Accepts both standard functions and coroutines for the predicate.

    Example:

        def pred(x):
            return x < 4

        async for value in takewhile(pred, range(8)):
            ...  # 0, 1, 2, 3

    """
    if asyncio.iscoroutinefunction(predicate):
        async for item in iter(iterable):
            if await predicate(item):
                yield item
            else:
                break
    else:
        async for item in iter(iterable):
            if predicate(item):
                yield item
            else:
                break


def tee(itr: AnyIterable, n: int = 2) -> Tuple[AsyncIterator[T], ...]:
    """
    Return n iterators that each yield items from the given iterable.

    The first iterator lazily fetches from the original iterable, and then
    queues the values for the other iterators to yield when needed.

    Caveat: all iterators are dependent on the first iterator – if it is
    consumed more slowly than the rest, the other consumers will be blocked
    until the first iterator continues forward.  Similarly, if the first
    iterator is consumed more quickly than the rest, more memory will be
    used in keeping values in the queues until the other iterators finish
    consuming them.

    Example:

        it1, it2 = tee(range(5), n=2)

        async for value in it1:
            ...  # 0, 1, 2, 3, 4

        async for value in it2:
            ...  # 0, 1, 2, 3, 4

    """
    assert n > 0
    sentinel = object()
    queues = [asyncio.Queue() for k in range(n)]

    async def gen(k: int, q: asyncio.Queue) -> AsyncIterator[T]:
        if k == 0:
            async for value in iter(itr):
                await asyncio.gather(*[queue.put(value) for queue in queues[1:]])
                yield value

            await asyncio.gather(*[queue.put(sentinel) for queue in queues[1:]])

        else:
            while True:
                value = await q.get()
                if value is sentinel:
                    break
                yield value

    return tuple(gen(k, q) for k, q in builtins.enumerate(queues))


async def zip_longest(
    *itrs: AnyIterable, fillvalue: T = None
) -> AsyncIterator[Sequence[Optional[T]]]:
    """
    Yield a tuple of items from mixed iterables until all are consumed.

    If shorter iterables are exhausted, the default value will be used
    until all iterables are exhausted.

    Example:

        a = range(3)
        b = range(5)

        async for a, b in zip_longest(a, b, fillvalue=-1):
            a  # 0, 1, 2, -1, -1
            b  # 0, 1, 2,  3,  4

    """
    its: List[AsyncIterator[T]] = [iter(itr) for itr in itrs]
    itr_count = len(its)

    while True:
        values = await asyncio.gather(
            *[it.__anext__() for it in its], return_exceptions=True
        )
        finished = 0
        for idx, value in builtins.enumerate(values):
            if isinstance(value, AnyStop):
                finished += 1
                values[idx] = fillvalue
            elif isinstance(value, BaseException):
                raise value
        if finished >= itr_count:
            break
        yield tuple(values)
