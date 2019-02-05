# Copyright 2018 John Reese
# Licensed under the MIT license

import inspect
from typing import Awaitable, Union

from .types import T


async def maybe_await(object: Union[Awaitable[T], T]) -> T:
    if inspect.isawaitable(object):
        return await object  # type: ignore
    return object  # type: ignore
