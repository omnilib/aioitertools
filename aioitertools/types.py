# Copyright 2018 John Reese
# Licensed under the MIT license

from typing import Iterable, Iterator, AsyncIterable, AsyncIterator, TypeVar, Union

R = TypeVar("R")
T = TypeVar("T")

AnyIterable = Union[Iterable[T], AsyncIterable[T]]
AnyIterableIterable = Union[Iterable[AnyIterable], AsyncIterable[AnyIterable]]
AnyIterator = Union[Iterator[T], AsyncIterator[T]]
AnyStop = (StopIteration, StopAsyncIteration)
