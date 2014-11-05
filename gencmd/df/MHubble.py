# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, division

import numpy as np

class MHubble():
    def __init__(self, rc, cut=False):

        self._rc = rc
        if cut:
            self._cut = cut
        else:
            self._cut = 5000*rc

    def _cdf(self, r):

        rc = self._rc
        rcut = self._cut
        cdf = rc**2*np.pi*np.log(1+r**2/rc**2)
        return cdf

    def sample(self, n=100):

        rc = self._rc
        rcut = self._cut
        norm =   self._cdf(rcut)

        x = np.random.rand(n)
        invcdf = lambda U: rc*np.sqrt( (np.exp( (x*norm)/(np.pi*rc**2)) -1))

        r = invcdf(x)
        if self._cut:
            r = r[(r < self._cut)]
        theta = 2*np.pi*np.random.rand(len(r))

        return r, theta
