#!/usr/bin/env python

from dhaffner import builtins

import unittest


class TestCommon(unittest.TestCase):

    def test_dictmap(self):
        d = {'a': 1, 'b': 2, 'c': 3}
        dct = builtins.dictmap(lambda k, v: (k + 'dictmap', v + 1), d)
        self.assertEqual(dct.get('adictmap'), 2)

    def test_dictfilter(self):
        d = {'a': 10, 'b': 20, 'c': 30}
        dct = builtins.dictfilter(lambda k, v: v >= 20, d)
        self.assertTrue(dct['b'] == 20)
        self.assertTrue('c' in dct and dct['c'] == 30)
        self.assertTrue('a' not in dct)

    def test_dictattrgetter(self):
        dag = builtins.dictattrgetter('rfind', 'capitalize')
        dct = dag(str)
        self.assertTrue(len(dct.keys()) == 2)
        self.assertTrue(callable(dct['rfind']))
        self.assertTrue('capitalize' in dct)

    def test_dictitemgetter(self):
        d = {'a': 100, 'b': 200, 'c': 300}
        dag = builtins.dictitemgetter('a', 'b')
        dct = dag(d)
        self.assertTrue(len(dct.keys()) == 2)
        self.assertTrue(dct['a'] == 100)
        self.assertTrue('c' not in dct)

    def test_lazyproperty(self):
        from random import random

        class TestLazyProperty(object):

            @builtins.lazyproperty
            def mylazyprop(self):
                return random()

        tlp = TestLazyProperty()
        j = tlp.mylazyprop
        self.assertTrue(j > 0)

        self.assertTrue(hasattr(tlp, 'mylazyprop'))
        del tlp.mylazyprop

        k = tlp.mylazyprop
        self.assertTrue(k > 0 and j != k)

    def setUp(self):
        pass
