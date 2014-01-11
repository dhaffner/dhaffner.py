__all__ = ('filter', 'filterfalse', 'map', 'range', 'reduce', 'zip',
           'compose', 'star', 'unstar', 'PY2', 'PY3')

from sys import version_info

PY3 = version_info[0] == 3
PY2 = version_info[0] == 2

if PY3:
    from itertools import filterfalse

elif PY2:
    from itertools import ifilterfalse as filterfalse


def unstar(func):
    return lambda args: func(*args)


def compose(*funcs):
    return reduce(lambda f, g: lambda x: f(g(x)), funcs)


def sifter(*funcs):

    def sift(x):
        for f in funcs:
            if not f(x):
                return False
        return True

    return sift
