#!/usr/bin/env python

import functions
import iterators

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


class TestIterators(unittest.TestCase):
    def setUp(self):
        pass

    def test_compact(self):
        lst = [False] * 5 + [True] * 10
        lst = list(iterators.compact(lst))

        length = len(lst)
        self.assertTrue(length == 10)

        lst = list(iterators.compact(lst))
        self.assertTrue(len(lst) == length)

    def test_consume(self):
        it = iter(xrange(10))
        iterators.consume(it, 3)
        self.assertTrue(next(it) == 3)

        iterators.consume(it)
        self.assertRaises(StopIteration, next, it)

    def test_dotproduct(self):
        v1, v2 = xrange(1, 10), xrange(10, 19)
        p = iterators.dotproduct(v1, v2)
        self.assertTrue(p == 690)

    def test_drop(self):
        gen = iterators.drop(xrange(10), 1)
        self.assertTrue(next(gen) == 1)

    def test_exhaust(self):
        it = iter('teststring')
        iterators.exhaust(it)
        self.assertRaises(StopIteration, next, it)

    def test_first(self):
        lst = ['A', 'B', 'C', 'D']
        self.assertTrue(iterators.first(lst) == 'A')

        gen = xrange(20, 30)
        self.assertTrue(iterators.first(gen) == 20)

        self.assertRaises(StopIteration, iterators.first, [])

    def test_flatten(self):
        lst = []
        for i in [10, 20, 30]:
            lst.append(list(xrange(i)))

        flat_lst = list(iterators.flatten(lst))
        self.assertTrue(len(flat_lst) == 60)

    def test_issequence(self):
        self.assertTrue(iterators.issequence([]))
        self.assertTrue(iterators.issequence([1, 2, 3]))
        self.assertTrue(iterators.issequence(x for x in [1, 2]))
        self.assertFalse(iterators.issequence(1))
        self.assertFalse(iterators.issequence('string'))




if __name__ == '__main__':
    unittest.main()
