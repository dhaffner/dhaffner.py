
from dhaffner import iterators

import unittest


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
        it = iter(range(10))
        iterators.consume(it, 3)
        self.assertTrue(next(it) == 3)

        iterators.consume(it)
        self.assertRaises(StopIteration, next, it)

    def test_cons(self):
        it = iterators.cons(1, range(10, 20))
        self.assertTrue(next(it) == 1)
        self.assertTrue(next(it) == 10)


    def test_dotproduct(self):
        v1, v2 = range(1, 10), range(10, 19)
        p = iterators.dotproduct(v1, v2)
        self.assertTrue(p == 690)

    def test_drop(self):
        gen = iterators.drop(range(10), 1)
        self.assertTrue(next(gen) == 1)

    def test_exhaust(self):
        it = iter('teststring')
        iterators.exhaust(it)
        self.assertRaises(StopIteration, next, it)

    def test_first(self):
        lst = ['A', 'B', 'C', 'D']
        self.assertTrue(iterators.first(lst) == 'A')

        gen = range(20, 30)
        self.assertTrue(iterators.first(gen) == 20)

        self.assertTrue(iterators.first([], None) == None)
        self.assertTrue(iterators.first([], 'poo') == 'poo')

        self.assertRaises(StopIteration, iterators.first, [])

    def test_flatten(self):
        lst = []
        for i in [10, 20, 30]:
            lst.append(list(range(i)))

        flat_lst = list(iterators.flatten(lst))
        self.assertTrue(len(flat_lst) == 60)

    def test_ilen(self):
        self.assertTrue(iterators.ilen(range(100)) == 100)
        self.assertTrue(iterators.ilen(['a', 'b', 'c']) == 3)
        self.assertTrue(iterators.ilen([]) == 0)

    def test_isiterable(self):
        self.assertTrue(iterators.isiterable([]))
        self.assertTrue(iterators.isiterable([1, 2, 3]))
        self.assertTrue(iterators.isiterable(x for x in [1, 2]))
        self.assertFalse(iterators.isiterable(1))
        self.assertFalse(iterators.isiterable('string', strings=False))
        self.assertTrue(iterators.isiterable('string', strings=True))

    def test_iterate(self):
        f = iterators.iterate(lambda x: x ** 2, 2)
        self.assertEqual(next(f), 4)
        self.assertEqual(next(f), 16)

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
        lst = range(1000)
        fit, tit = iterators.partition(lst, pred)
        D = [next(fit) - next(tit)] * 500
        self.assertTrue(D.count(1) == 500)

    def test_pick(self):
        it = iterators.pick(range(10))
        iterators.consume(it, 10)
        picks = [next(it)] * 10
        self.assertTrue(picks.count(9) == 10)

    def test_powerset(self):
        it = iterators.powerset(range(3))
        self.assertTrue(iterators.isiterable(it))
        lst = list(it)
        self.assertTrue(
            lst == [(), (0,), (1,), (2,), (0, 1), (0, 2), (1, 2), (0, 1, 2)]
        )

    def test_split(self):
        head, tail = iterators.split(range(10))
        self.assertTrue(head == 0)
        self.assertTrue(iterators.isiterable(tail))

    def test_take(self):
        lst = iterators.take(10, range(100))
        self.assertTrue(iterators.last(lst) == 9)
        self.assertEqual(iterators.last([1]), 1)

    def test_unique(self):
        it = iterators.unique([10, 20, 30, 40, 50] * 3)
        self.assertTrue(iterators.ilen(it) == 5)

    def test_with_iter(self):
        from contextlib import contextmanager

        @contextmanager
        def f():
            yield range(12, 22)

        c = iterators.with_iter(f())
        self.assertTrue(next(c) == 12)

    def test_where(self):
        d1 = {'a': 1, 'b': 2, 'c': 3, 'd': 33}
        d2 = {'a': 10, 'b': 2, 'c': 3, 'd': 8}

        w1 = iterators.where([d1, d2], a=10)
        self.assertEqual(iterators.ilen(w1), 1)

        w2 = iterators.where([d1, d2], b=2, c=3)
        self.assertEqual(iterators.ilen(w2), 2)


if __name__ == '__main__':
    unittest.main()
