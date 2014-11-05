# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, division

import numpy as np

class Hubble():
    def __init__(self, rc, cut=False):

        self._rc = rc
        self._cut = cut

    #not invertible
    def _cdf(self, rc, x):
        return (rc**2)*(rc/(rc+x) + np.log(rc + x))

    def sample(self, n=100):

        rc = self._rc
        cut = self._cut
        x = np.random.rand(n)
        invcdf = lambda rc, U: (rc/(1-U)) - rc

        r = invcdf(rc, x)
        if cut:
            r = r[(r < cut)]
        theta = 2*np.pi*np.random.rand(len(r))

        return r, theta
