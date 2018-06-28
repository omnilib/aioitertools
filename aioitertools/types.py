# Copyright 2018 John Reese
# Licensed under the MIT license

from typing import (
    Any,
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

AnyFunction = Union[Callable[..., R], Callable[..., Awaitable[R]]]
AnyIterable = Union[Iterable[T], AsyncIterable[T]]
AnyIterableIterable = Union[Iterable[AnyIterable], AsyncIterable[AnyIterable]]
AnyIterator = Union[Iterator[T], AsyncIterator[T]]
AnyStop = (StopIteration, StopAsyncIteration)
Accumulator = Union[Callable[[T, T], T], Callable[[T, T], Awaitable[T]]]
KeyFunction = Union[Callable[..., Any], Callable[..., Awaitable[Any]]]
Predicate = Union[Callable[..., bool], Callable[..., Awaitable[bool]]]
