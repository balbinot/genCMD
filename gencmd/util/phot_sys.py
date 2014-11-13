#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, division

import numpy as np

col_dict = {'sdss': 'm_ini, m_act, u, g, r, i, z, J, H, Ks',
            'des': 'm_ini, m_act, u, g, r, i, z, Y'}

ecoeff = { 'sdss': {'u': [0.001, 23.4, 1.3],
                    'g': [0.001, 23.4, 1.3],
                    'r': [0.001, 23.4, 1.3],
                    'i': [0.001, 23.4, 1.3],
                    'z': [0.001, 23.4, 1.3],
                    'J': [0.001, 23.4, 1.3],
                    'H': [0.001, 23.4, 1.3],
                    'Ks':[0.001, 23.4, 1.3]},
          # Balbinot et al 2014, submitted
          'des': {'u': [0.002, 26.00, 1.3],
                  'g': [0.002, 26.41, 1.25],
                  'r': [0.002, 26.34, 1.27],
                  'i': [0.003, 25.52, 1.34],
                  'z': [0.003, 24.75, 1.43],
                  'Y': [0.009, 23.45, 1.40]}
          }

