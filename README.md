aioitertools
============

itertools for AsyncIO and mixed iterables.

[![build status](https://travis-ci.org/jreese/aioitertools.svg?branch=master)](https://travis-ci.org/jreese/aioitertools)
[![version](https://img.shields.io/pypi/v/aioitertools.svg)](https://pypi.org/project/aioitertools)
[![license](https://img.shields.io/pypi/l/aioitertools.svg)](https://github.com/jreese/aioitertools/blob/master/LICENSE)
[![code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


Install
-------

aioitertools requires Python 3.6 or newer.
You can install it from PyPI:

    $ pip3 install aioitertools


Usage
-----

aioitertools shadows the standard library whenever possible to provide
asynchronous version of the modules and functions you already know.  It's
fully compatible with standard iterators and async iterators alike, giving
you one unified, familiar interface for interacting with iterable objects:

    from aioitertools import iter, next, map, zip

    something = iter(...)
    first_item = await next(something)

    async for item in iter(something):
        ...


    async def fetch(url):
        response = await aiohttp.request(...)
        return response.json

    async for value in map(fetch, MANY_URLS):
        ...


    async for a, b in zip(something, something_else):
        ...


See [builtins.py][builtins] for full documentation.



License
-------

aioitertools is copyright [John Reese](https://jreese.sh), and licensed under
the MIT license.  I am providing code in this repository to you under an open
source license.  This is my personal repository; the license you receive to
my code is from me and not from my employer. See the `LICENSE` file for details.


[builtins]: https://github.com/jreese/aioitertools/blob/master/aioitertools/builtins.py
