#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testgencmd))
    return suite


if __name__ == '__main__':

    #unittest.main()
    suiteFew = unittest.TestSuite()
    suiteFew.addTest(testgencmd("testKroupa"))
    unittest.TextTestRunner(verbosity=2).run(suite())
