# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, division

import numpy as np
import os
from scipy import interpolate
import sqlite3

from .. import df

col_dict = {'sdss': 'm_ini, m_act, u, g, r, i, z, J, H, Ks',
            'des': 'm_ini, m_act, u, g, r, i, z, Y'}

class SSP(object):
    def __init__(self, age, met, mf='kroupa', **kwargs):

        self.age = age
        self.met = met

        self._ISOCDIR = kwargs['isocdir']

        try:
           self.isoc = self._getiso(group=kwargs['group'],
                                    filterset=kwargs['filterset'])
        except:
           self.isoc = self._getiso()

        self.max_mass = np.max(self.isoc[:,0])
        self.min_mass = np.min(self.isoc[:,0])

        if mf == 'kroupa':
            try:
                # Try to use values given by user.
                self.mf = df.Kroupa(kwargs['a'], kwargs['mlim'])
            except:
                # Fall back to default if not given
                self.mf = df.Kroupa()
        elif mf == 'user':
            try:
                self.mf = df.UserMF(kwargs['mass'])
            except:
                print("Give me a mass array")
                raise ValueError
        elif mf == 'texp':
            # Not implemented
            # self.mf = df.TaperedExp()
            raise ValueError("Not implemented")
        else:
            raise ValueError("Not implemented or inexistent")

    def populate(self, n=10000, fbin=0.0):

        flux = lambda x: 10**(-x/2.5)

        self.n = n
        try:
            masses = self.mf.sample(n)
        except:
            # User mass array
            masses = self.mf.sample()

        # Total mass sampled from the full IMF
        total_mass = sum(masses)

        # Mask to exclude values outside the range covered by the model
        mask = (masses < self.max_mass)&(masses > self.min_mass)
        masses = masses[mask]
        n = len(masses)

        ivals = self._interpolate()
        stars = np.array(masses)
        for vname in self.cols[1:]:
            stars = np.c_[stars, ivals[vname](masses)]

        if fbin > 0.0:
            print("Binaries are buggy, beware")
            magic = 0.63
            idx = np.random.randint(int(n*fbin), size=int((1.0/magic)*n*fbin))
            cmasses = self.mf.sample(len(idx))
            for i, vname in enumerate(self.cols[2:]):
                stars[idx, i+2] = -2.5*np.log10(flux(stars[idx, i+2]) +
                                                flux(ivals[vname](cmasses)))

        elif 1.0 < fbin < 0.0:
            raise ValueError("f_bin must be less than 1 and positive")

        self._stars = stars
        self._total_mass = total_mass

        return total_mass, stars

    def _getiso (self, group='padova12', filterset='des'):
        """
        Find the corresponding isochrone for a given age and metallicity
        """

        age = self.age
        met = self.met

        _ISOCDIR = self._ISOCDIR

        table_name = 'padova_'+filterset
        self.cols = col_dict[filterset].split()

        print(_ISOCDIR)
        connection=sqlite3.connect(_ISOCDIR+'/isoc_'+group+'_'+filterset+'.sqlite')
        cursor=connection.cursor()

        # this return a list of tuples
        cursor.execute('SELECT Z_met FROM met_grid ORDER BY ABS(Z_met - '+str(met)+') LIMIT 1')
        n_Z = cursor.fetchall()[0][0]

        cursor.execute('SELECT lage FROM age_grid ORDER BY ABS(lage - '+str(age)+') LIMIT 1')
        n_age = cursor.fetchall()[0][0]

        if float(n_Z) != met or float(n_age) != age:
            print("Model with Z = "+str(met)+" and log(age/yr) = "+str(age)+" not found.")
            print("Using Z = "+str(n_Z)+" and log(age/yr) = "+str(n_age))
        else:
            print("Using Z = "+str(n_Z)+" and log(age/yr) = "+str(n_age))

        age = str(n_age)
        met = str(n_Z)
        cursor.execute('SELECT '+ col_dict[filterset] +' FROM '+table_name+' WHERE lage = '+age+' AND Z_met = '+met)
        self.isoc = np.asarray(cursor.fetchall())
        self.age = n_age
        self.met = n_Z

        return self.isoc

    def _interpolate(self):
        """
        This method can be generalized to interpolate any quantity given in the
        isochrone table.

        NOTES:
            - higher order interpolation are broken. Scipy.interpolate.interp1d
              does not provide a good solution. Why?
        """
        m = {}
        z = self.isoc[:,0] # mass array
        for idx, name in enumerate(self.cols):
            m[name] = interpolate.interp1d(z, self.isoc[:,idx],
                                           bounds_error=False)

        return m

    def _setisocdir(self, dir):

        self._ISOCDIR = dir
        return
