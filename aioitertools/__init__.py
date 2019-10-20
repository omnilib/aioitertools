# Copyright 2018 John Reese
# Licensed under the MIT license

"""
itertools for AsyncIO and mixed iterables
"""

__author__ = "John Reese"
__version__ = "0.4.0"

from . import asyncio
from .builtins import enumerate, iter, list, map, next, set, sum, zip
from .itertools import (
    accumulate,
    chain,
    combinations,
    combinations_with_replacement,
    compress,
    count,
    cycle,
    dropwhile,
    filterfalse,
    groupby,
    islice,
    permutations,
    product,
    repeat,
    starmap,
    takewhile,
    tee,
    zip_longest,
)
