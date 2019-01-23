# Copyright 2018 John Reese
# Licensed under the MIT license

from typing import (
    Callable,
    Iterable,
    Iterator,
    AsyncIterable,
    AsyncIterator,
    Awaitable,
    TypeVar,
    Union,
)

R = TypeVar("R")
T = TypeVar("T")
N = TypeVar("N", int, float)

AnyFunction = Union[Callable[..., R], Callable[..., Awaitable[R]]]
AnyIterable = Union[Iterable[T], AsyncIterable[T]]
AnyIterableIterable = Union[Iterable[AnyIterable[T]], AsyncIterable[AnyIterable[T]]]
AnyIterator = Union[Iterator[T], AsyncIterator[T]]
AnyStop = (StopIteration, StopAsyncIteration)
Accumulator = Union[Callable[[T, T], T], Callable[[T, T], Awaitable[T]]]
KeyFunction = Union[Callable[[T], R], Callable[[T], Awaitable[R]]]
Predicate = Union[Callable[[T], object], Callable[[T], Awaitable[object]]]
