# Copyright 2018 John Reese
# Licensed under the MIT license

from typing import (
    AsyncIterable,
    AsyncIterator,
    Awaitable,
    Callable,
    Iterable,
    Iterator,
    TypeVar,
    Union,
)

R = TypeVar("R")
T = TypeVar("T")
T1 = TypeVar("T1")
T2 = TypeVar("T2")
T3 = TypeVar("T3")
T4 = TypeVar("T4")
T5 = TypeVar("T5")
N = TypeVar("N", int, float)

AnyFunction = Union[Callable[..., R], Callable[..., Awaitable[R]]]
AnyIterable = Union[Iterable[T], AsyncIterable[T]]
AnyIterableIterable = Union[Iterable[AnyIterable[T]], AsyncIterable[AnyIterable[T]]]
AnyIterator = Union[Iterator[T], AsyncIterator[T]]
AnyStop = (StopIteration, StopAsyncIteration)
Accumulator = Union[Callable[[T, T], T], Callable[[T, T], Awaitable[T]]]
KeyFunction = Union[Callable[[T], R], Callable[[T], Awaitable[R]]]
Predicate = Union[Callable[[T], object], Callable[[T], Awaitable[object]]]
