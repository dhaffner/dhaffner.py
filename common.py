__all__ = ('compose', 'map', 'filter', 'filterfalse', 'reduce', 'range', 'zip',
           'wraps', 'PY2', 'PY3')

from sys import version_info, hexversion

PY3 = version_info[0] == 3
PY2 = version_info[0] == 2

if PY3:
    from functools import reduce
    from itertools import filterfalse
    map = map
    filter = filter
    range = range
    reduce = reduce
    zip = zip

elif PY2:
    from itertools import (imap as map, ifilter as filter,
                           ifilterfalse as filterfalse, izip as zip)
    range = xrange
    reduce = reduce

# functools.wraps
if hexversion < 0x030300b1:
    from functools import partial, WRAPPER_ASSIGNMENTS, WRAPPER_UPDATES

    def update_wrapper(wrapper, wrapped, assigned=WRAPPER_ASSIGNMENTS,
                       updated=WRAPPER_UPDATES):
        wrapper.__wrapped__ = wrapped
        for attr in assigned:
            try:
                value = getattr(wrapped, attr)
            except AttributeError:
                pass
            else:
                setattr(wrapper, attr, value)
        for attr in updated:
            getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
        return wrapper

    def wraps(wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES):
        return partial(update_wrapper, wrapped=wrapped, assigned=assigned, updated=updated)

else:
    from functools import wraps
    wraps = wraps


def compose(*funcs):
    """Compose a sequence of functions.

    >>> compose(f, g)(x) = f(g(x))
    """
    return reduce(lambda g, h: lambda *args, **kwargs: g(h(*args, **kwargs)), funcs)
