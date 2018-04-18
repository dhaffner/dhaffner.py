#!/usr/bin/env python
import unittest

from dhaffner import misc, iterators


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

        lines = misc.lazysplit(s)
        self.assertTrue(iterators.isiterable(lines))
        self.assertTrue(iterators.ilen(lines) == 5)
