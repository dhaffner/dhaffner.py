#!/usr/bin/env python

from dhaffner import functions

import random
import unittest
import time
import operator

class TestFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_caller(self):
        caller = functions.caller(['one', 'two'])
        self.assertEqual('onetwo', caller(operator.add))

    def test_atomize(self):
        pass

    def test_flip(self):
        f = functions.flip(operator.sub)
        self.assertEqual(f(2, 1), -1)

    def test_constant(self):
        f = functions.constant('A')
        self.assertTrue(f(1) == 'A')
        self.assertTrue(f() == 'A')
        self.assertTrue(f([1, 2]) == 'A')

    def test_context(self):
        f = functions.context(lambda x: x  ** 2, 2)
        with f as y:
            self.assertTrue(y == 4)

    def test_nargs(self):
        self.assertTrue(functions.nargs(self.test_nargs) == 1)

    def test_curry(self):
        f = functions.curry(lambda x, y: x + y)
        self.assertTrue(callable(f(1)))
        self.assertTrue(f(1)(2) == 3)

    def test_identity(self):
        self.assertTrue(functions.identity(1) == 1)

    def test_iterate(self):
        f = functions.iterate(lambda x: x ** 2, 2)
        self.assertEqual(next(f), 4)
        self.assertEqual(next(f), 16)

    def test_pipe(self):
        lst = [3, 2, 1]
        f = functions.pipe(list.sort)
        self.assertTrue(f(lst) == [1, 2, 3])

    def test_scan(self):
        f = lambda a, b: a + b
        lst1 = list(functions.scan(f, [1, 2, 3], 0))
        lst2 = list(functions.scan(f, [1, 2, 3]))

        self.assertEqual(lst1, [0, 1, 3, 6])
        self.assertEqual(lst2, [2, 4, 7])

    def test_vectorize(self):
        f = functions.vectorize(lambda a: a)

        self.assertTrue(f(1) == [1])
        self.assertTrue(f((1,2)) == (1, 2))

        gen = xrange(2)
        self.assertTrue(f(gen) == gen)


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
