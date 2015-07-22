# -*- coding: utf-8 -*-
''':class:`functions` Some high-order functions and decorators.'''

__all__ = ('atomize', 'caller', 'composable', 'compose', 'constant',
           'context', 'curry', 'flip', 'identity', 'juxt', 'nargs', 'pipe',
           'scan', 'vectorize')

import operator

from contextlib import contextmanager
from functools import partial, wraps
from inspect import getargspec
from threading import RLock

from six.moves import map, reduce

from dhaffner.iterators import compact, first, last, isiterable, iterate, take
from dhaffner.common import compose


def atomize(func, lock=None):
    """Decorate `func` with a reentrant lock to prevent multiple threads
    from calling said `func` simultaneously.

    :argument func: the function to decorate
    :argument lock: the lock to use (optional)
    """

    if lock is None:
        lock = RLock()

    @wraps(func)
    def atomic(*args, **kwargs):
        with lock:
            return func(*args, **kwargs)

    return atomic


def caller(args, kwargs=None):
    """Return a lambda that takes a callable as input and applies it to the
    given arguments.
    """
    return lambda func: func(*args, **(kwargs or {}))


def compose2(*funcs):

    def apply(func, args):
        if not isiterable(args):
            args = [args]
        return func(*args)

    return reduce(lambda f, g: lambda x: apply(f, g(x)), funcs)


def flip(func):
    """Decorate the given function to reverse the order of its arguments."""
    @wraps(func)
    def flipped(*args, **kwargs):
        return func(*reversed(args), **kwargs)

    return flipped


class composable(object):  # noqa
    def __init__(self, func=lambda x: x, *args, **kwargs):
        self.func = partial(func, *args, **kwargs) if (args or kwargs) else func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def wrap(self, *funcs):
        funcs = funcs + (self.func, )
        return self.__class__(compose(*funcs))

    def juxt(self, func, other):
        return self.__class__(compose2(func, juxt(self.func, other)))

    def __add__(self, other, add=operator.add):
        return self.juxt(add, other)

    def __sub__(self, other, sub=operator.sub):
        return self.juxt(sub, other)

    def __mul__(self, other, mul=operator.mul):
        return self.juxt(mul, other)

    def __floordiv__(self, other, floordiv=operator.floordiv):
        return self.juxt(floordiv, other)

    __divmod__ = __floordiv__

    def __mod__(self, other, mod=operator.mod):
        return self.juxt(mod, other)

    def __and__(self, other, and_=operator.and_):
        return self.juxt(and_, other)

    def __xor__(self, other, xor=operator.xor):
        return self.juxt(xor, other)

    def __or__(self, other, or_=operator.or_):
        return self.juxt(or_, other)

    def __div__(self, other, div=operator.div):
        return self.juxt(div, other)

    def __truediv__(self, other, truediv=operator.truediv):
        return self.juxt(truediv, other)

    def __lt__(self, other, lt=operator.lt):
        return self.juxt(lt, other)

    def __le__(self, other, le=operator.le):
        return self.juxt(le, other)

    def __eq__(self, other, eq=operator.eq):
        return self.juxt(eq, other)

    def __ne__(self, other, ne=operator.ne):
        return self.juxt(ne, other)

    def __ge__(self, other, ge=operator.ge):
        return self.juxt(ge, other)

    def __gt__(self, other, gt=operator.gt):
        return self.juxt(gt, other)

    # iterate
    def __pow__(self, n):
        func = compose(last, partial(take, n), partial(iterate, self.func))
        return self.__class__(func)

    def __neg__(self, neg=operator.neg):
        return self.wrap(neg)

    def __pos__(self, pos=operator.pos):
        return self.wrap(pos)

    def __abs__(self, abs=operator.abs):
        return self.wrap(abs)

    def __invert__(self, invert=operator.invert):
        return self.wrap(invert)

    __inv__ = __invert__

    def __lshift__(self, other):
        return self.__class__(compose(self.func, other))

    def __rshift__(self, other):
        return self.wrap(other)

    def __str__(self):
        return str(self.func)

    def __repr__(self):
        return repr(self.func)


def constant(x):
    """Close x under an anonymous function."""
    return lambda *args, **kwargs: x


@contextmanager
def context(func, *args, **kwargs):
    """Return a context for lazily evaluating a function with given input."""
    yield func(*args, **kwargs)


# Return the number of position arguments in the given function.
nargs = compose(partial(reduce, operator.sub),
                partial(map, len),
                compact,
                operator.attrgetter('args', 'defaults'),
                getargspec)


def curry(func, n=None):
    """Curry a function for up to n arguments, where by default n is the number
    of fixed, unnamed arguments in the function defintion.
    """

    if n is None:
        n = nargs(func)

    def curried(*args, **kwargs):
        if len(args) >= n:
            return func(*args, **kwargs)
        return curry(partial(func, *args, **kwargs), n - len(args))

    return curried


def identity(x):
    """Identity function; return the input unchanged."""
    return x


def juxt(*funcs):
    """Return a function whose positional arguments are determined by
    evaluating each function in funcs with the given *args, and **kwargs. If
    funcs = [f1, f2, ...], this is equivalent to:

    return lambda *a, **k: func(f1(*a, **k), f2(*a, **k), ...)
    """
    def inner(*args, **kwargs):
        return (f(*args, **kwargs) for f in funcs)
    return inner


def pipe(func):
    """Return a function which evaluates func for a given input and returns the
    input. Useful for wrapping functions which do not return a useful input,
    such as print.
    """
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


def vectorize(func):
    """Decorate a function to always return a sequence rather than a scalar."""

    @wraps(func)
    def wrapped(*args, **kwargs):
        value = func(*args, **kwargs)
        return value if isiterable(value) else [value]

    return wrapped
