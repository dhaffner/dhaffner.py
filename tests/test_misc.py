#!/usr/bin/env python

from dhaffner import misc, iterators

import random
import unittest
import time
import operator


class TestMisc(unittest.TestCase):

    def setUp(self):
        pass

    def test_files(self):
        files = misc.files('.', '*')
        self.assertTrue(iterators.isiterable(files))


    def test_find(self):
        s = "This is a 1234, test."
        m = misc.find('(\d+)', s)
        self.assertEqual(m, '1234')
        self.assertEqual(misc.find('(aaa)', s, default='blah'), 'blah')
        self.assertRaises(StopIteration, misc.find, '(aaa)', s)


    def test_maybe(self):
        lst = []
        f = lambda x: lst.append(x)
        for i in xrange(10):
            misc.maybe(1.0, f, 'A')
            misc.maybe(0.0, f, 'B')

        self.assertTrue(lst.count('A') == 10)
        self.assertTrue(lst.count('B') == 0)

    def test_noop(self):
        self.assertEqual(misc.noop(), None)
        self.assertEqual(misc.noop(1), None)
        self.assertEqual(misc.noop(2, blah=1), None)

    def test_splitlines(self):
        s = \
        """a
        b
        c
        d
        e"""

        lines = misc.splitlines(s)
        self.assertTrue(iterators.isiterable(lines))
        self.assertTrue(iterators.length(lines) == 5)
