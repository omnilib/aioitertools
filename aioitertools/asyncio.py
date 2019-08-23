# Copyright 2019 John Reese
# Licensed under the MIT license

"""
Friendlier version of asyncio standard library.

Provisional library.  Must be imported as `aioitertools.asyncio`.
"""

import asyncio
import time
from typing import Any, Awaitable, Dict, Iterable, List, Optional, Set, Tuple, cast

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


async def gather(
    *args: Awaitable[T],
    loop: Optional[asyncio.AbstractEventLoop] = None,
    return_exceptions: bool = False,
    limit: int = -1
) -> List[Any]:
    """Like asyncio.gather but with a limit on concurrency.

    Much of the complexity of gather comes with it support for cancel, which we
    omit here.  Note that all results are buffered.
    """

    # For detecting input duplicates and reconciling them at the end
    input_map: Dict[Awaitable[T], List[int]] = {}
    # This is keyed on what we'll get back from asyncio.wait
    pos: Dict[asyncio.Future[T], int] = {}
    ret: List[Any] = [None] * len(args)

    pending: Set[asyncio.Future[T]] = set()
    done: Set[asyncio.Future[T]] = set()

    next_arg = 0

    while True:
        while next_arg < len(args) and (limit == -1 or len(pending) < limit):
            # We have to defer the creation of the Task as long as possible
            # because once we do, it starts executing, regardless of what we
            # have in the pending set.
            if args[next_arg] in input_map:
                input_map[args[next_arg]].append(next_arg)
            else:
                # We call ensure_future directly to ensure that we have a Task
                # because the return value of asyncio.wait will be an implicit
                # task otherwise, and we won't be able to know which input it
                # corresponds to.
                task: asyncio.Future[T] = asyncio.ensure_future(args[next_arg])
                pending.add(task)
                pos[task] = next_arg
                input_map[args[next_arg]] = [next_arg]
            next_arg += 1

        # pending might be empty if the last items of args were dupes;
        # asyncio.wait([]) will raise an exception.
        if pending:
            done, pending = await asyncio.wait(
                pending, loop=loop, return_when=asyncio.FIRST_COMPLETED
            )
            for x in done:
                if return_exceptions and x.exception():
                    ret[pos[x]] = x.exception()
                else:
                    ret[pos[x]] = x.result()

        if not pending and next_arg == len(args):
            break

    for lst in input_map.values():
        for i in range(1, len(lst)):
            ret[lst[i]] = ret[lst[0]]

    return ret
