'''
Some helper functions around Python built-in types: "numerics, sequences,
mappings, files, classes, instances and exceptions."
'''

__all__ = ('dictfilter', 'dictitemgetter', 'dictmap')


from operator import attrgetter, itemgetter

from six import iteritems
from six.moves import map, filter, zip


#
#   Dictionaries
#


def dictmap(func, d):
    return dict(map(func, iteritems(d)))


def dictfilter(func, d):
    return dict(filter(func, iteritems(d)))


def dictgetter(getterfunc):  # Not included in __all__

    def getter(*keys):
        keys = tuple(keys)
        values = getterfunc(*keys)
        return lambda obj: dict(zip(keys, values(obj)))

    return getter


dictattrgetter = dictgetter(attrgetter)


dictitemgetter = dictgetter(itemgetter)


#
#   Properties
#


class lazyproperty(property):
    """A decorator to lazily evaluate an object property."""
    def __init__(self, *args):
        self.__called__ = False
        super(lazyproperty, self).__init__(*args)

    def __get__(self, obj, type=None):
        if obj is None:
            return None
        elif self.__called__:
            value = self.__value__
        else:
            value = self.__value__ = self.fget(obj)
            self.__called__ = True
        return value

    def __delete__(self, obj):
        if self.__called__:
            self.__called__ = False
            del self.__value__
