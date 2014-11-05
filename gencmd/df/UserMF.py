# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, division

class UserMF():
    """
    Just a class to provide compatible access to a user given mass array
    """
    def __init__(self, mass):
        self.mass = mass

    def sample(self):
        return self.mass
