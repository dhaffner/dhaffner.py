#!/usr/bin/env python

# Some functions on sequences and iterables.

__all__ = ('compact', 'consume', 'drop', 'exhaust', 'first', 'flatten',
           'issequence', 'last', 'nth', 'pick', 'reusable', 'split', 'tag',
           'take', 'unique')

from collections import deque, Sequence
from functools import partial
from itertools import islice, chain, tee
from operator import mul

from six.moves import map, filter

from common import compose, filterfalse


# Remove false values from sequence.
compact = partial(filter, bool)


def consume(iterator, n=None, next=next, islice=islice, deque=deque):
    """Consume a given amount of elements in from a generator. If no amount is
    specified, exhaust the entire sequence.
    """
    if n is not None:
        next(islice(iterator, n, n), None)
    else:
        deque(iterator, maxlen=0)


def dotproduct(vec1, vec2, sum=sum, map=map, mul=mul):
    """Compute and return the dot product of two vectors (sequences)."""
    return sum(map(mul, vec1, vec2))


def drop(iterable, n, islice=islice):
    """Drop the first n elements of the given iterable."""
    return islice(iterable, n, None)


def exhaust(iterator, deque=deque):
    """Exhaust a given iterator."""
    deque(iterator, maxlen=0)


# Get first element of a sequence
first = compose(next, iter)


# Flatten a sequence one level of iteration.
flatten = chain.from_iterable


def issequence(obj, isinstance=isinstance, Sequence=Sequence):
    """Determine whether obj is a sequence. Strings are not considered
    sequences.
    """

    try:
        obj.strip
    except:
        pass
    else:
        return False

    return isinstance(obj, Sequence)


# Get the last element of an iterable.
last = partial(reduce, lambda _, y: y)


def nth(iterable, n, next=next, islice=islice, default=None):
    """Returns the nth item or a default value

    http://docs.python.org/3.4/library/itertools.html#itertools-recipes
    """
    return next(islice(iterable, n, None), default)


def pick(iterable):
    """Yield elements of sequence, repeating the last element infinitely after
    the sequence is iterated over."""
    for element in iterable:
        yield element
    while True:
        yield element


class reusable(object):
    def __init__(self, iterable):
        self.iterable = iterable

    def __iter__(self):
        return self

    def reset(self):
        """Reset the iterator to the start. Discard any remaining values in the
        current iteration.
        """
        self.iterator, self.iterable = tee(self.iterable)

    def next(self):
        try:
            return next(self.iterator)
        except StopIteration:
            self.reset()
            raise


# Return a tuple containing the next element in the sequence,
# and an iterable containing the rest of the sequence.
split = compose(lambda iterator, next=next: (next(iterator), iterator), iter)


def take(n, iterable, islice=islice):
    """Take the first n elements of the given iterable."""
    return islice(iterable, n)


def unique(iterable, filterfalse=filterfalse):
    """Return only unique elements from the sequence."""
    seen = set()
    add = seen.add
    for element in filterfalse(seen.__contains__, iterable):
        add(element)
        yield element

