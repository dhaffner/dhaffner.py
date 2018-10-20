__all__ = ('compose', 'sifter')

from six.moves import reduce


def compose(*funcs):
    return reduce(lambda f, g: lambda x: f(g(x)), funcs)


def sifter(*funcs):
    def sift(x):
        for f in funcs:
            if not f(x):
                return False
        return True

    return sift
