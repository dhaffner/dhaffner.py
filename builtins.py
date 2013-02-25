#!/usr/bin/env python

# Some helper functions around Python built-in types: "numerics, sequences,
# mappings, files, classes, instances and exceptions."
#
# Might delete this module later if it seems unnecessary.

__all__ = ('dictfilter', 'dictitemgetter', 'dictmap', 'throws')

from operator import attrgetter, itemgetter

from common import map, zip


def dictmap(func, dictionary):
    return dict(zip(dictionary.iterkeys(), map(func, dictionary.itervalues())))


def dictfilter(func, dictionary):
    return dict((key, value) for (key, value) in dictionary.iteritems() \
                if func(value))


def dictgetter(getterfunc):  # Not included in __all__

    def getter(*keys):
        keys = tuple(keys)
        values = getterfunc(*keys)
        return lambda obj: dict(zip(keys, values(obj)))

    return getter


dictattrgetter = dictgetter(attrgetter)


dictitemgetter = dictgetter(itemgetter)


def throws(thunk, exception):
    if isinstance(exception, Exception):
        exception = (exception, )
    try:
        thunk()
    except exception:
        return True
    else:
        return False
