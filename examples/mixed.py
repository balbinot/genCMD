#!/usr/bin/env python
#-*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as p

from gencmd.model import SSP
from gencmd.util import phot_sys

gerr = phot_sys.ecoeff['des']['g']
rerr = phot_sys.ecoeff['des']['r']

def err(m, a, b, c):
    return a + np.exp((m-b)/c)

isocdir = '/scratch/isocdir/'  # Change me!

lAges = np.linspace(7,10.15,300)
Z = np.zeros_like(lAges) + 0.015/10

# Set up IMF in reasonable mass values
imf = 'kroupa'
mlim = [0.7, 2.0, 120.0]
slope = [2.35, 2.0]

ratios = (10**lAges[1:]-10**lAges[:-1])/(10**lAges[-1] - 10**lAges[-2])

n0 = 1000
N = n0*ratios

dmod = 15.49 # Some distance modulus

p.figure(figsize=(5,8))
for la, z, n in zip(lAges, Z, N):

    # Create population object
    pop = SSP(la, z, mf=imf, a=slope, mlim=mlim, isocdir=isocdir)

    # Sample from the IMF and interpolate on the isocrone n0 points
    Tmass, stars = pop.populate(n=n)

    g = stars[:,3] + dmod
    r = stars[:,4] + dmod

    g = g + np.random.randn(len(g))*err(g, *gerr)
    r = r + np.random.randn(len(r))*err(r, *rerr)

    p.plot(g-r, g, 'k.', ms=1)

p.xlabel('g-r')
p.ylabel('g')
p.ylim(22,11)
p.xlim(-1,1.5)

p.show()

