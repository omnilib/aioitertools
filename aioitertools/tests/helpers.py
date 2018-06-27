# Copyright 2018 John Reese
# Licensed under the MIT license

import asyncio


def async_test(fn):
    def wrapped(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(fn(*args, **kwargs))

    return wrapped
