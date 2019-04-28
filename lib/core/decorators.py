#!/usr/bin/env python2
# coding=utf-8

"""
Copyright (c) 2006-2019 sqlmap developers (http://sqlmap.org/)
See the file 'LICENSE' for copying permission
"""

import functools
import hashlib
import threading

from lib.core.settings import MAX_CACHE_ITEMS
from lib.core.datatype import LRUDict
from lib.core.threads import getCurrentThreadData

_lock = threading.Lock()


def cachedmethod(f, cache=LRUDict(capacity=MAX_CACHE_ITEMS)):
    """
    Method with a cached content

    Reference: http://code.activestate.com/recipes/325205-cache-decorator-in-python-24/
    """

    @functools.wraps(f)
    def _(*args, **kwargs):
        key = int(hashlib.md5("|".join(str(_) for _ in (f, args, kwargs))).hexdigest(), 16) & 0x7fffffffffffffff

        try:
            with _lock:
                result = cache[key]
        except KeyError:
            result = f(*args, **kwargs)

            with _lock:
                cache[key] = result

        return result

    return _


def stackedmethod(f):
    """
    Method using pushValue/popValue functions (fallback function for stack realignment)
    """

    @functools.wraps(f)
    def _(*args, **kwargs):
        threadData = getCurrentThreadData()
        originalLevel = len(threadData.valueStack)

        try:
            result = f(*args, **kwargs)
        finally:
            if len(threadData.valueStack) > originalLevel:
                threadData.valueStack = threadData.valueStack[:originalLevel]

        return result

    return _
