#!/usr/bin/env python


#
#   Experimental replacements for functions.compose and functions.merge
#


def compose(f, g):
    source = \
    """def composed(*args, **kw):
    return f(g(*args, **kw))"""
    exec compile(source, '<string>', 'single') in locals()
    return locals().get('composed')


def merge(func, *funcs):
    funcs = tuple(funcs)

    symbols = dict(('f{}'.format(i), f) for i, f in enumerate(funcs))
    call = '{}(*args, **kwargs)'.format

    source = """def merged(*args, **kwargs):
    return func({})"""
    source = source.format(', '.join(call(f) for f in sorted(symbols.iterkeys())))

    symbols['func'] = func
    exec compile(source, '<string>', 'single') in symbols
    return symbols.get('merged')
