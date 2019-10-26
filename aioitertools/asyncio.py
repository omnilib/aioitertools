# Copyright 2019 John Reese
# Licensed under the MIT license

"""
Friendlier version of asyncio standard library.

Provisional library.  Must be imported as `aioitertools.asyncio`.
"""

import asyncio
import time
from typing import Any, Awaitable, Dict, Iterable, List, Optional, Set, Union, cast

from .types import AsyncIterator, T


async def as_completed(
    aws: Iterable[Union[asyncio.Future, Awaitable[T]]],
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
    done: Set[asyncio.Future[T]] = set()
    tmp: Set[asyncio.Future[T]]

    # Basically _FutureT from typeshed asyncio/tasks.pyi; we have to define this
    # longhand or it ends up with Any instead of T
    pending: Set[Union[asyncio.Future, Awaitable[T]]] = set(aws)
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

        done, tmp = await asyncio.wait(
            pending, loop=loop, timeout=remaining, return_when=asyncio.FIRST_COMPLETED
        )

        # in mypy at least, you can't assign an Set[A] to a Set[Union[A, B]]
        # without an error.  This cast allows us to do so while still retaining
        # type checks everywhere else.
        pending = cast(Set[Union[asyncio.Future, Awaitable[T]]], tmp)

        for item in done:
            yield await item
