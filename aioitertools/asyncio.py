# Copyright 2019 John Reese
# Licensed under the MIT license

"""
Friendlier version of asyncio standard library.

Provisional library.  Must be imported as `aioitertools.asyncio`.
"""

import asyncio
import time
from typing import Awaitable, Iterable, Optional, Set

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

        done, pending = await asyncio.wait(  # type: ignore # bad annotation upstream
            pending, loop=loop, timeout=remaining, return_when=asyncio.FIRST_COMPLETED
        )

        for item in done:
            yield await item
