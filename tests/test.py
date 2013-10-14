#!/usr/bin/env python

from dhaffner import functions, iterators

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

    def test_isiterable(self):
        self.assertTrue(iterators.isiterable([]))
        self.assertTrue(iterators.isiterable([1, 2, 3]))
        self.assertTrue(iterators.isiterable(x for x in [1, 2]))
        self.assertFalse(iterators.isiterable(1))
        self.assertFalse(iterators.isiterable('string', strings=False))
        self.assertTrue(iterators.isiterable('string', strings=True))

    def test_length(self):
        self.assertTrue(iterators.length(xrange(100)) == 100)
        self.assertTrue(iterators.length(['a', 'b', 'c']) == 3)
        self.assertTrue(iterators.length([]) == 0)

    def test_last(self):
        lst = [10, 20, 30]
        self.assertTrue(iterators.last(lst) == 30)

    def test_nth(self):
        lst = [10, 20, 30]
        self.assertTrue(iterators.nth(lst, 1) == 20)
        self.assertTrue(iterators.nth(lst, 10) == None)
        self.assertTrue(iterators.nth(lst, 10, default=100) == 100)

    def test_partition(self):
        pred = lambda x: x % 2 == 0
        lst = xrange(1000)
        fit, tit = iterators.partition(lst, pred)
        D = [next(fit) - next(tit)] * 500
        self.assertTrue(D.count(1) == 500)

    def test_pick(self):
        it = iterators.pick(xrange(10))
        iterators.consume(it, 10)
        picks = [next(it)] * 10
        self.assertTrue(picks.count(9) == 10)

    def test_split(self):
        head, tail = iterators.split(xrange(10))
        self.assertTrue(head == 0)
        self.assertTrue(iterators.isiterable(tail))

    def test_take(self):
        lst = iterators.take(10, xrange(100))
        self.assertTrue(iterators.last(lst) == 9)

    def test_unique(self):
        it = iterators.unique([10, 20, 30, 40, 50] * 3)
        self.assertTrue(iterators.length(it) == 5)


if __name__ == '__main__':
    unittest.main()
