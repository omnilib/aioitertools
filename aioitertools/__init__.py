# Copyright 2018 John Reese
# Licensed under the MIT license

"""
itertools for AsyncIO and mixed iterables
"""

__author__ = "John Reese"
__version__ = "0.2.0"

from .builtins import iter, next, list, set, enumerate, map, sum, zip
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
