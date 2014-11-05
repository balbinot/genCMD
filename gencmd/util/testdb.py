#!/usr/bin/env python
from sys import argv
import numpy as np

Zlist = np.array([])

agelist = np.loadtxt(argv[1], usecols=(0,))

agelist = np.unique(agelist)

for fname in argv[1:]:
    a = open(fname, 'r')
    line = a.readline()
    while '#' in line:
        if 'Isochrone' in line:
            Z = line.split()[4]
            Zlist = np.r_[Zlist, float(Z)]
            line = " "
        else:
            line = a.readline()
    a.close()

print agelist
print Zlist

