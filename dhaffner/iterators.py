#!/usr/bin/env python

# Some functions on sequences and iterables.

__all__ = ('compact', 'consume', 'drop', 'exhaust', 'first', 'flatten',
           'isiterable', 'length', 'last', 'nth', 'pick', 'split', 'take', 'unique')

from collections import deque, Iterable
from functools import partial
from itertools import islice, chain, tee
from operator import mul

from six.moves import map, filter

from dhaffner.common import compose, filterfalse


# Remove false values from sequence.
compact = partial(filter, bool)


def consume(iterator, n=None, next=next, islice=islice, deque=deque):
    """
    Consume a given amount of elements in from a generator. If no amount is
    specified, exhaust the entire sequence.
    """
    if n is not None:
        next(islice(iterator, n, n), None)
    else:
        exhaust(iterator)


def dotproduct(vec1, vec2, sum=sum, map=map, mul=mul):
    """
    Compute and return the dot product of two vectors (sequences).
    """
    return sum(map(mul, vec1, vec2))


def drop(iterable, n, islice=islice):
    """
    Drop the first n elements of the given iterable.
    """
    return islice(iterable, n, None)


# Exhaust a given iterator.
exhaust = deque(maxlen=0).extend


# Get first element of a sequence
first = compose(next, iter)


# Flatten a sequence one level of iteration.
flatten = chain.from_iterable


def isiterable(obj, strings=False, isinstance=isinstance, Iterable=Iterable):
    """
    Determine whether obj is a sequence.
    """
    return (isinstance(obj, Iterable) and
            not (isinstance(obj, basestring) and not strings))


def length(iterable):
    return sum(1 for x in iterable)



# Get the last element of an iterable.
_last_deque = deque(maxlen=1)
def last(iterable, extend=_last_deque.extend, pop=_last_deque.pop):
    extend(iterable)
    return pop()


def nth(iterable, n, next=next, islice=islice, default=None):
    """
    Return the nth item or a default value from an iterable.

    http://docs.python.org/3.4/library/itertools.html#itertools-recipes
    """
    return next(islice(iterable, n, None), default)


def partition(items, predicate=bool):
    """
    Partition a given sequence into two  subsequences: those for which
    predicate returns True and those for which it returns False.

    Source: http://nedbatchelder.com/blog/201306/filter_a_list_into_two_parts.html
    """

    a, b = tee((predicate(item), item) for item in items)
    return ((item for pred, item in a if not pred),
            (item for pred, item in b if pred))


# TODO: better name for this function
def pick(iterable):
    """
    Yield elements of sequence, repeating the last element infinitely after
    the sequence is iterated over.
    """
    for element in iterable:
        yield element
    while True:
        yield element


# Return a tuple containing the next element in the sequence,
# and an iterable containing the rest of the sequence.
split = compose(lambda iterator, next=next: (next(iterator), iterator), iter)


def take(n, iterable, islice=islice):
    """
    Take the first n elements of the given iterable.
    """
    return islice(iterable, n)


def unique(iterable, filterfalse=filterfalse):
    """
    Return only unique elements from the sequence.
    """
    seen = set()
    add = seen.add
    for element in filterfalse(seen.__contains__, iterable):
        add(element)
        yield element


def where(dicts, **kwargs):
    def sift(d):
        for (k, v) in kwargs.iteritems():
            if d.get(k) != v:
                return False
        return True

    return filter(sift, dicts)
