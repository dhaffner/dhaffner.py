#!/usr/bin/env python

from dhaffner import common

import random
import unittest
import time
import operator


class TestCommon(unittest.TestCase):

    def setUp(self):
        pass

    def test_sifter(self):
        s = common.sifter(lambda x: x > 5, lambda x: x % 2 == 1)
        lst = list(filter(s, xrange(20)))
        self.assertEqual(len(lst), 7)

    def test_compose(self):
        c = common.compose(lambda x: x + 2, lambda y: y ** 2)
