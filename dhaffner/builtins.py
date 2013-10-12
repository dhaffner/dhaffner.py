'''
Some helper functions around Python built-in types: "numerics, sequences,
mappings, files, classes, instances and exceptions."
'''

__all__ = ('dictfilter', 'dictitemgetter', 'dictmap', 'throws')


from functools import partial
from itertools import takewhile
from operator import attrgetter, itemgetter, methodcaller

from six import iterkeys, itervalues
from six.moves import map, filter, zip

from dhaffner.common import compose


#
#   Dictionaries
#


def dictmap(func, dictionary):
    return dict(zip(iterkeys(dictionary), map(func, itervalues(dictionary))))


def dictfilter(func, dictionary):
    return dict((key, value) for (key, value) in dictionary.iteritems()
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
#   Tuples
#


class composite(tuple):
    def __getattr__(self, name):

        def attrs(*args, **kwargs):
            return self.map(methodcaller(name, *args, **kwargs))

        return attrs

    def map(self, func):
        return self.__class__(map(func, self))

    def filter(self, func):
        return self.__class__(filter(func, self))


class vector(object):
    def __init__(self, iterable):
        self.v = iterable

    def map(self, *funcs):
        func = compose(*reversed(funcs))
        self.v = map(func, self.v)
        return self

    def filter(self, *funcs):
        self.v = filter(vector.sift(funcs), self.v)
        return self

    def takewhile(self, *funcs):
        self.v = takewhile(vector.sift(funcs), self.v)
        return self

    def __iter__(self):
        return iter(self.v)

    @staticmethod
    def sift(funcs):
        return lambda x: all(func(x) for func in funcs)

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
