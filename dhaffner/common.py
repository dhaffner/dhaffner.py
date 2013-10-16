__all__ = ('filter', 'filterfalse', 'map', 'range', 'reduce', 'wraps', 'zip',
           'compose', 'star', 'unstar', 'PY2', 'PY3')

from functools import partial
from sys import version_info, hexversion

PY3 = version_info[0] == 3
PY2 = version_info[0] == 2

if PY3:
    from itertools import filterfalse

elif PY2:
    from itertools import ifilterfalse as filterfalse


# functools.wraps
if hexversion < 0x030300b1:
    from functools import WRAPPER_ASSIGNMENTS, WRAPPER_UPDATES

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


def unstar(func):
    return lambda args: func(*args)


def compose(*funcs):
    return reduce(lambda f, g: lambda x: f(g(x)), funcs)
