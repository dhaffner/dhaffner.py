#!/usr/bin/env python

import functions, misc, iterators

import random
import unittest
import time
import operator

# functions
#__all__ = ('atomize', 'cache', 'caller', 'composable', 'compose', 'constant',
#           'context', 'curry', 'flip', 'identity', 'iterate', 'memoize',
#           'merge', 'pipe', 'scan', 'uncurry', 'vectorize', 'wraps')




class TestFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_cache(self):
        cached = functions.cache(seconds=2)(random.random)
        v = cached()
        time.sleep(1)

        self.assertEqual(v, cached())

    def test_caller(self):
        caller = functions.caller(['one', 'two'])
        self.assertEqual('onetwo', caller(operator.add))


class TestFunctionsComposable(unittest.TestCase):
    def setUp(self):
        self.ops = ['add', 'sub', 'mul', 'floordiv', 'mod', 'and_', 'xor', 'or_',
               'div', 'truediv']

    def test_ops(self):
        ops = operator.attrgetter(*self.ops)(operator)
        f = lambda x: x ** 2
        g = lambda y: y > 10 and y - 5 or y * 3

        f = functions.composable(f)
        g = functions.composable(g)

        for op in ops:
            h = op(f, g)
            self.assertTrue(callable(h))

            start = random.randint(100, 200)

            for n in xrange(start, start + 100):
                self.assertEqual(h(n), op(f(n), g(n)))

if __name__ == '__main__':
    unittest.main()
