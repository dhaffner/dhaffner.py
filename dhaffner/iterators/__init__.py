# Some functions on sequences and iterables.

__all__ = (
    'compact',
    'cons',
    'consume',
    'drop',
    'exhaust',
    'first',
    'flatten',
    'ilen',
    'isiterable',
    'iterate',
    'last',
    'nth',
    'pick',
    'split',
    'take',
    'unique'
)

from collections import deque, Iterable
from functools import partial
from itertools import combinations, chain, islice, tee
from operator import mul

from six.moves import map, filter, filterfalse

from dhaffner.common import compose


# Remove false values from sequence.
compact = partial(filter, bool)


def cons(element, sequence):
    """Add element to beginning of (possibly infinite) sequence.
    >>> list(cons(1, [2, 3]))
    [1, 2, 3]
    """
    yield element
    for s in sequence:
        yield s


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


def first(sequence, default=Ellipsis):
    """Get first element of a sequence"""
    if default is Ellipsis:
        return next(iter(sequence))
    else:
        return next(iter(sequence), default)


# Flatten a sequence one level of iteration.
flatten = chain.from_iterable


def isiterable(obj, strings=False, isinstance=isinstance, Iterable=Iterable):
    """
    Determine whether obj is a sequence.
    """
    return (isinstance(obj, Iterable) and
            not (isinstance(obj, str) and not strings))


def iterate(func, x):
    """Return a generator that will repeatedly call a function with a given
    initial input, feeding the resulting value back into said function."""
    while True:
        x = func(x)
        yield x


def ilen(iterable):
    return sum(1 for x in iterable)


_last_deque = deque(maxlen=1)


def last(iterable, extend=_last_deque.extend, pop=_last_deque.pop):
    '''Get the last element of an iterable.'''
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


def powerset(iterable):
    """Yields all possible subsets of the iterable
        >>> list(powerset([1,2,3]))
        [(), (1,), (2,), (3,), (1, 2), (1, 3), (2, 3), (1, 2, 3)]
    """
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


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


def with_iter(contextmanager):
    """Wrap an iterable in a ``with`` statement, so it closes once exhausted.
    For example, this will close the file when the iterator is exhausted::
        upper_lines = (line.upper() for line in with_iter(open('foo')))
    Any context manager which returns an iterable is a candidate for
    ``with_iter``.
    """
    with contextmanager as iterable:
        for item in iterable:
            yield item


def where(dicts, **kwargs):
    def sift(d):
        for (k, v) in kwargs.items():
            if d.get(k) != v:
                return False
        return True

    return filter(sift, dicts)
