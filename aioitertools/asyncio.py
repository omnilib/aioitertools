# Copyright 2019 John Reese
# Licensed under the MIT license

"""
Friendlier version of asyncio standard library.

Provisional library.  Must be imported as `aioitertools.asyncio`.
"""

import asyncio
import time
from typing import Awaitable, Iterable, Optional, Set, Tuple, cast

from .types import AsyncIterator, T


async def as_completed(
    aws: Iterable[Awaitable[T]],
    *,
    loop: Optional[asyncio.AbstractEventLoop] = None,
    timeout: Optional[float] = None
) -> AsyncIterator[T]:
    """
    Run awaitables in `aws` concurrently, and yield results as they complete.

    Unlike `asyncio.as_completed`, this yields actual results, and does not require
    awaiting each item in the iterable.

    Example:

        async for value in as_completed(futures):
            ...  # use value immediately

    """
    done: Set[Awaitable[T]] = set()
    pending: Set[Awaitable[T]] = set(aws)
    remaining: Optional[float] = None

    if timeout and timeout > 0:
        threshold = time.time() + timeout
    else:
        timeout = None

    while pending:
        if timeout:
            remaining = threshold - time.time()
            if remaining <= 0:
                raise asyncio.TimeoutError()

        # asyncio.Future inherits from typing.Awaitable
        # asyncio.wait takes Iterable[Union[Future, Generator, Awaitable]], but
        # returns Tuple[Set[Future], Set[Future]. Because mypy doesn't like assigning
        # these values to existing Set[Awaitable] or even Set[Union[Awaitable, Future]],
        # we need to first cast the results to something that we can actually use
        # asyncio.Future: https://github.com/python/typeshed/blob/72ff7b94e534c610ddf8939bacbc55343e9465d2/stdlib/3/asyncio/futures.pyi#L30
        # asyncio.wait(): https://github.com/python/typeshed/blob/72ff7b94e534c610ddf8939bacbc55343e9465d2/stdlib/3/asyncio/tasks.pyi#L89
        done, pending = cast(
            Tuple[Set[Awaitable[T]], Set[Awaitable[T]]],
            await asyncio.wait(
                pending,
                loop=loop,
                timeout=remaining,
                return_when=asyncio.FIRST_COMPLETED,
            ),
        )

        for item in done:
            yield await item
