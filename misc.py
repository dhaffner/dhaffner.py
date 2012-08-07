#!/usr/bin/env python

# Miscellaneous functions.

__all__ = ('files', 'find', 'maybe', 'noop', 'splitlines', 'throws', 'unescape')

import fnmatch
import functools
import htmlentitydefs
import itertools
import os
import random
import re


def files(directory, pattern):
    """Return all filenames from directory which match given pattern."""
    join = functools.partial(os.path.join, directory)
    return itertools.imap(join, fnmatch.filter(os.listdir(directory), pattern))


def find(pattern, string, default=None):
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

    return match.group(0)


def maybe(p, func, x):
    """With probability p, evaluate func(x). Always return x."""
    if random.random() <= p:
        func(x)
    return x


def noop(*args, **kwargs):
    """Do nothing."""
    pass


def splitlines(text, exp=re.compile(r'^.*$', re.MULTILINE)):
    """Split lines in the given string lazily."""
    for match in exp.finditer(text):
        yield match.group(0)


def throws(thunk, exception):
    if isinstance(exception, Exception):
        exception = (exception, )
    try:
        thunk()
    except exception:
        return True
    else:
        return False


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
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text  # leave as-is

    return re.sub("&#?\w+;", fixup, text)
