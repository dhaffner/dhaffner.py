#!/usr/bin/env python

# Some helper functions around Python built-in types: "numerics, sequences,
# mappings, files, classes, instances and exceptions."
#
# Might delete this module later if it seems unnecessary.

__all__ = ('dictfilter', 'dictitemgetter', 'dictmap')

from operator import itemgetter

from common import map, zip


def dictmap(func, dictionary):
    return dict(zip(dictionary.iterkeys(), map(func, dictionary.itervalues())))


def dictfilter(func, dictionary):
    return dict((key, value) for (key, value) in dictionary.iteritems() \
                if func(value))


def dictitemgetter(*keys):
    keys = tuple(keys)
    getvalues = itemgetter(*keys)

    def getter(dictionary):
        return dict(zip(keys, getvalues(dictionary)))

    return getter
