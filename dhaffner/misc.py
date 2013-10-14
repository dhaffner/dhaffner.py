"""
Miscellaneous functions.
"""

__all__ = ('files', 'find', 'maybe', 'noop', 'splitlines', 'unescape')

import re

from contextlib import contextmanager
from fnmatch import filter as fnmatch_filter
from functools import partial
from os import listdir, path
from random import random

from six.moves import map

from dhaffner.common import PY3

if PY3:
    from html.entities import name2codepoint
else:
    from htmlentitydefs import name2codepoint


def files(directory, pattern):
    """Return all filenames from directory which match given pattern."""
    join = partial(path.join, directory)
    return map(join, fnmatch_filter(listdir(directory), pattern))


def find(pattern, string, default=None, n=0):
    """Return the first match from a search for pattern in string."""
    matches = re.finditer(pattern, string)
    # If a default was specified, handle a potential exception.
    # Otherwise, let the exception be handled elsewhere.
    try:
        match = next(matches)
    except StopIteration:  # no matches
        if default is None:
            raise
        return default

    return match.group(n)


def maybe(p, func, x):
    """With probability p, evaluate func(x). Always return x."""
    if random() <= p:
        func(x)
    return x


def noop(*args, **kwargs):
    """Do nothing."""
    pass


def splitlines(text, exp=re.compile(r'^.*$', re.MULTILINE)):
    """Split lines in the given string lazily."""
    for match in exp.finditer(text):
        yield match.group(0)


def unescape(text):
    """Unescape HTML characters in the input.
    """
    def fixup(m):
        text = m.group(0)
        if text.startswith("&#"):
            # character reference
            try:
                if text.startswith("&#x"):
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1], 10))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text  # leave as-is

    return re.sub("&#?\w+;", fixup, text)


@contextmanager
def signalcontext(signalnum, callback):
    import signal

    def handler(signalnum, frame):
        callback()

    signal.signal(signalnum, handler)
    yield
    signal.pause()
