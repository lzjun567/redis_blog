#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple
from functools import wraps
from functools import wraps


def cache(func):
    caches = {}

    @wraps(func)
    def wrap(*args):
        if args not in caches:
            caches[args] = func(*args)
        return caches[args]

    return wrap


@cache
def fib(n):
    print 'hello'
    if n < 2:
        return 1
    return fib(n - 1) + fib(n - 2)


if __name__ == "__main__":
   print ",".join(['h'])
   print 'xxxxxxxx'[0:-2]
