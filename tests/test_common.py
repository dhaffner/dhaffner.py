#!/usr/bin/env python

from dhaffner import common

import unittest


class TestCommon(unittest.TestCase):

    def setUp(self):
        pass

    def test_sifter(self):
        s = common.sifter(lambda x: x > 5, lambda x: x % 2 == 1)
        lst = list(filter(s, range(20)))
        self.assertEqual(len(lst), 7)

    def test_compose(self):
        c = common.compose(lambda x: x + 2, lambda y: y ** 2)
        self.assertEqual(c(12), 146)
