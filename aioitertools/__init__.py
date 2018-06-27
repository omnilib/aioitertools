# Copyright 2018 John Reese
# Licensed under the MIT license

"""
itertools for AsyncIO and mixed iterables
"""

__author__ = "John Reese"
__version__ = "0.1.0"

from .builtins import iter, next, list, set, enumerate, map, sum, zip
from .itertools import count, cycle, repeat
from .types import AnyIterable
