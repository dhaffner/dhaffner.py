"""
Miscellaneous functions.
"""

__all__ = ('files', 'find', 'noop', 'splitlines')

import re

from fnmatch import filter as fnfilter
from functools import partial
from os import listdir, path

from six.moves import map


def files(directory, pattern):
    """Return all filenames from directory which match given pattern."""
    join = partial(path.join, directory)
    return map(join, fnfilter(listdir(directory), pattern))


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


def noop(*args, **kwargs):
    """Do nothing."""
    pass


def splitlines(text, exp=re.compile(r'^.*$', re.MULTILINE)):
    """Split lines in the given string lazily."""
    for match in exp.finditer(text):
        yield match.group(0)
