#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

"""
test_gencmd
----------------------------------

Tests for `gencmd` module.
"""

import unittest
import gencmd

class testgencmd(unittest.TestCase):
    """ Test class for gencmd """

    def setUp(self):

        self.kroupa_sampler = gencmd.df.Kroupa()
        pass

    def testKroupa(self):
        self.assertEqual(len(self.kroupa_sampler.sample(10)), 10)
