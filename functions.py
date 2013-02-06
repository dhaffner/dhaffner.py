#!/usr/bin/env python

# Some high-order functions and decorators.

__all__ = ('atomize', 'cache', 'caller', 'composable', 'compose', 'constant',
           'context', 'curry', 'flip', 'identity', 'iterate', 'memoize',
           'merge', 'pipe', 'scan', 'uncurry', 'vectorize', 'wraps')

import operator

from contextlib import contextmanager
from functools import partial
from inspect import getargspec
from sys import hexversion
from threading import RLock
from time import time

from iterators import compact, first, last, issequence, take
from common import compose, map, filter, reduce, wraps, unstar


def atomize(func, lock=None):
    """
    Decorate a function with a reentrant lock to prevent multiple
    threads from calling said thread simultaneously.
    """

    if lock is None:
        lock = RLock()

    @wraps(func)
    def atomic(*args, **kwargs):
        with lock:
            return func(*args, **kwargs)

    return atomic


# @cached(seconds=100)
# def f(x, y=False):
#     ...
#
def cache(seconds=0):

    def key(func, args, kwargs):
        return (args, frozenset((kwargs or {}).iteritems()))

    def wrapper(func):
        _cache = {}

        def add(k):
            args, kwargs = k
            value = func(*args, **dict(kwargs))
            _cache[k] = (time(), value)
            return value

        @wraps(func)
        def wrapped(*args, **kwargs):
            k = key(func, args, kwargs)
            if k in _cache:
                t, v = _cache.get(k)
                if (time() - t) <= seconds:
                    return v
            return add(k)

        return wrapped

    return wrapper


def caller(args, kwargs=None):
    """Return a lambda that takes a callable as input and applies it to the given arguments.
    """
    return lambda func: func(*args, **(kwargs or {}))


def flip(func):
    """Decorate the given function to reverse the order of its arguments."""
    @wraps(func)
    def flipped(*args, **kwargs):
        return func(*reversed(args), **kwargs)

    return flipped


class composable(object):
    def __init__(self, func=lambda x: x, *args, **kwargs):
        self.func = partial(func, *args, **kwargs) if (args or kwargs) else func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def compose(self, *funcs):
        return self.__class__(compose(*funcs))

    def merge(self, func, other):
        return self.__class__(merge(func, self, other))

    def __add__(self, other, add=operator.add):
        return self.merge(add, other)

    def __sub__(self, other, sub=operator.sub):
        return self.merge(sub, other)

    def __mul__(self, other, mul=operator.mul):
        return self.merge(mul, other)

    def __floordiv__(self, other, floordiv=operator.floordiv):
        return self.merge(floordiv, other)

    __divmod__ = __floordiv__

    def __mod__(self, other, mod=operator.mod):
        return self.merge(mod, other)

    def __and__(self, other, and_=operator.and_):
        return self.merge(and_, other)

    def __xor__(self, other, xor=operator.xor):
        return self.merge(xor, other)

    def __or__(self, other, or_=operator.or_):
        return self.merge(or_, other)

    def __div__(self, other, div=operator.div):
        return self.merge(div, other)

    def __truediv__(self, other, truediv=operator.truediv):
        return self.merge(truediv, other)

    def __lt__(self, other, lt=operator.lt):
        return self.merge(lt, other)

    def __le__(self, other, le=operator.le):
        return self.merge(le, other)

    def __eq__(self, other, eq=operator.eq):
        return self.merge(eq, other)

    def __ne__(self, other, ne=operator.ne):
        return self.merge(ne, other)

    def __ge__(self, other, ge=operator.ge):
        return self.merge(ge, other)

    def __gt__(self, other, gt=operator.gt):
        return self.merge(gt, other)

    # iterate
    def __pow__(self, n):
        return self.compose(last, partial(take, n), iterate(self))

    def __neg__(self, neg=operator.neg):
        return self.compose(neg, self)

    def __pos__(self, pos=operator.pos):
        return self.compose(pos, self)

    def __abs__(self, abs=operator.abs):
        return self.compose(abs, self)

    def __invert__(self, invert=operator.invert):
        return self.compose(invert, self)

    __inv__ = __invert__

    # compose
    def __lshift__(self, other):
        return self.compose(self, other)

    # __rshift__ = flip(__lshift__)

    # __radd__ = flip(__add__)

    # __rsub__ = flip(__sub__)

    # __rmul__ = flip(__mul__)

    # __rdiv__ = flip(__div__)

    # __rtruediv__ = flip(__truediv__)

    # __rfloordiv__ = flip(__floordiv__)

    # __rmod__ = flip(__mod__)

    # __rdivmod__ = flip(__divmod__)

    # __rlshift__ = flip(__lshift__)

    # __rrshift__ = flip(__rshift__)

    def __str__(self):
        return str(self.func)

    def __repr__(self):
        return repr(self.func)


def constant(x):
    """Close x under an anonymous function."""
    return lambda *args, **kwargs: x


@contextmanager
def context(func, *args, **kwargs):
    """Return a context for lazily evaluating a function for given input."""
    yield func(*args, **kwargs)


# def nargs(func):
#     args = operator.attrgetter('args', 'defaults')(getargspec(func))
#     return reduce(lambda a, b=0: a - b, map(len, filter(bool, args)))

nargs = compose(partial(reduce, operator.sub),
                partial(map, len),
                compact,
                operator.attrgetter('args', 'defaults'),
                getargspec)


def curry(func, n=None):
    """Curry a function for up to n arguments, where by default n is the number
    of fixed, unnamed arguments in func's defintion.
    """

    if n is None:
        n = nargs(func)

    @wraps(func)
    def curried(*args, **kwargs):
        if len(args) >= n:
            return func(*args, **kwargs)
        return curry(partial(func, *args, **kwargs), n - len(args))

    return curried


def identity(x):
    return x


def iterate(func, x):
    while True:
        x = func(x)
        yield x


# memoize is made obsolete as of Python 3.2 by functools.lru_cache.
if hexversion >= 0x03020000:
    from functools import lru_cache
    memoize = lru_cache(maxsize=None)

else:
    def memoize(func):
        """Memoization decorator. Caches a function's return value each time
        it is called. Return the cached value when it is called again with the
        same arguments. Does not support keyword arguments (yet).
        """
        cache = {}

        @wraps(func)
        def wrapped(*args):
            try:
                return cache[args]
            except KeyError:
                value = func(*args)
                cache[args] = value
                return value
            except TypeError:
                # uncachable.
                return func(*args)

        return wrapped


def merge(func, *funcs):
    """Return a function whose positional arguments are determined by
    evaluating each function in funcs with the given *args, and **kwargs. If
    funcs = [f1, f2, ...], this is equivalent to:

    return lambda *a, **k: func(f1(*a, **k), f2(*a, **k), ...)

    """
    call = lambda *args, **kwargs: map(caller(args, kwargs), funcs)
    return compose(unstar(func), call)


def pipe(func):
    """Return a function which evaluates func for a given input and returns the
    input. Useful for wrapping functions which do not return a useful input,
    such as print.
    """
    @wraps(func)
    def wrapped(x):
        func(x)
        return x

    return wrapped


def scan(func, sequence, init=None):
    if init is None:
        curr = first(sequence)
    else:
        curr = init
        yield init
    for element in sequence:
        curr = func(curr, element)
        yield curr


def uncurry(func):
    return lambda args=None, kwargs=None: func(*list(args or []), **(kwargs or {}))


def vectorize(func):
    """Decorate a function to always return a sequence rather than a scalar."""

    @wraps(func)
    def wrapped(*args, **kwargs):
        value = func(*args, **kwargs)
        return value if issequence(value) else [value]

    return wrapped
