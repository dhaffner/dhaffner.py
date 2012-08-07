#!/usr/bin/env python

# Some functions on sequences and iterables.

__all__ = ('compact', 'consume', 'drop', 'exhaust', 'first', 'flatten',
           'issequence', 'last', 'nth', 'pick', 'reusable', 'split', 'tag',
           'take', 'unique')

import collections
import functools
import itertools
import operator


def compact(sequence):
    """Remove false values from sequence."""
    return itertools.ifilter(bool, sequence)


def consume(sequence, n=None):
    """Consume a given amount of elements in from a generator. If no amount is
    specified, exhaust the entire sequence.
    """
    if n is not None:
        return itertools.islice(sequence, n, None)
    else:
        return exhaust(sequence)


def drop(sequence, n):
    return itertools.islice(sequence, n, None)


def exhaust(sequence):
    """Exhaust a given generator."""
    for _ in sequence:
        pass
    return


def first(sequence):
    """Get first element of a sequence"""
    return next(iter(sequence))


def flatten(sequences):
    """Flatten a sequence one level of iteration."""
    return itertools.chain.from_iterable(sequences)


def issequence(obj):
    """Determine whether obj is a sequence. Strings are not considered
    sequences.
    """

    try:
        obj.strip
    except:
        pass
    else:
        return False

    return isinstance(obj, collections.Sequence)


def last(sequence):
    """Get the last element of a sequence"""
    return reduce(lambda _, y: y, sequence)


def nth(n, pred, sequence):
    if pred is None:
        return last(take(n, sequence))
    else:
        return last(take(n, itertools.ifilter(pred, sequence)))


def pick(sequence):
    """Yield elements of sequence, repeating the last element infinitely after
    the sequence is iterated over."""
    for element in sequence:
        yield element
    while True:
        yield element


class reusable(object):
    def __init__(self, iterable):
        self.iterable = iterable

    def __iter__(self):
        return self

    def reset(self):
        """
        Resets the iterator to the start.

        Any remaining values in the current iteration are discarded.
        """
        self.iterator, self.iterable = itertools.tee(self.iterable)

    def next(self):
        try:
            return next(self.iterator)
        except StopIteration:
            self.reset()
            raise


def split(sequence):
    """Return a tuple containing the next element in the sequence,
    and an iterable containing the rest of the sequence.

    e.g.: head, tail = split(sequence)
    """
    iterable = iter(sequence)
    return next(iterable), iterable


def tag(t, sequence):
    """Tag (pair) t with each element in the given sequence"""
    return itertools.izip(itertools.repeat(t), sequence)


def take(n, sequence):
    return itertools.islice(sequence, n)


def unique(sequence):
    """Return only unique elements from the sequence."""
    seen = set()
    elements = itertools.ifilterfalse(functools.partial(operator.contains,
                                                        seen), sequence)
    for element in elements:
        seen.add(element)
        yield element
