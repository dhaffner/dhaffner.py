"""
Some helper functions around Python built-in types: "numerics, sequences,
mappings, files, classes, instances and exceptions."
Might delete this module later if it seems unnecessary.
"""

__all__ = ('dictfilter', 'dictitemgetter', 'dictmap', 'throws')

from operator import attrgetter, itemgetter

from common import map, zip


#
#   Dictionaries
#


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


#
#   Exceptions
#


def throws(thunk, exception):
    if isinstance(exception, Exception):
        exception = (exception, )
    try:
        thunk()
    except exception:
        return True
    else:
        return False


#
#   Properties
#


class lazyproperty(property):
    '''
    A decorator to lazily evaluate an object property.
    '''
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
