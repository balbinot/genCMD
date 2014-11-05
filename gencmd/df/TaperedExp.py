import numpy as np
from scipy import integrate, stats

__author__ = "Eduardo Balbinot (balbinot@if.ufrgs.br)"
__version__ = "$Revision: 0.1b $"
__copyright__ = "Copyright (c) 2011 Eduardo Balbinot"
__license__ = "BSD"

class TaperedExp():
    """An tapered exponential mass function f(x) ~ x^a * (1 - Exp(-(x/mc)**b)) """
    
    def __init__(self, normalize=True, a=-2.0, b=2.5, mc=0.15, mmin=0.08, mmax=20.0):
        """
        NAME:
            __init__
        PURPOSE:
            Initialize a tapered exponential DF f(x) ~ x^a * (1 - Exp(-(x/mc)**b))
        INPUT:
            normalize -- if True, normalize the DF to 1 (one). 
                         If number, normalize to number.
            a -- float (default = -2.0)
            b -- float (default = 2.5)
            mc -- float (default = 0.15)
            mmin, mmax -- mass range (large range equals low performance)
        OUTPUT:
        HISTORY:
            2011-03-30 - Written - Balbinot (UFRGS)
        """
        
        self._a = a
        self._b = b
        self._mc = mc
        self.mmin = mmin
        self.mmax = mmax

        if normalize:
            self._norm = self._normalize()
        else:
            self._norm = 1.0
        return None

    def eval(self, x):
        """
        NAME:
            eval
        PURPOSE:
            Evaluate the normalized DF at x
        INPUT:
            x -- number
        OUTPUT:
            DF(x) -- number 
        HISTORY:
            2011-03-30 - Written - Balbinot (UFRGS)
        """

        return self._norm*((x**self._a)*(1.0 - np.exp(-(x/self._mc)**self._b)))

    def sample(self, n=1):
        """
        NAME
            sample
        PURPOSE:
            Sample the DF
        INPUT:
            n -- integer. How many samples you want (default = 1)
        OUTPUT:
            if n > 1: array of floats
            if n = 1: float
        HISTORY:
            2011-03-30 - Written - Balbinot (UFRGS)
        """
        xmin, xmax = self.mmin, self.mmax
        h = np.max(self.eval(np.arange(xmin, 1.0, 0.0001)))
        x = []
        while len(x) < n:
            # It would be nice to improve this using a proper rejection method. 
            # What envelope function shoud we use? 
            u1 = np.random.rand()*(xmax - xmin) + xmin
            u2 = np.random.rand()*h
            if u2 <= self.eval(u1):
                x.append(u1)
        
        return x

    def _integrand(self, x):
        """ Whatenever needed for _normalize """

        return ((x**self._a)*(1 - np.exp(-(x/self._mc)**self._b)))

    def _normalize(self):
        """
        NAME
            _normalize
        PURPOSE:
            Normalize the DF
        INPUT:
        OUTPUT:
            number
        HISTORY:
            2011-03-30 - Written - Balbinot (UFRGS)
        """
        norm = 1.0
        norm /= integrate.quad(self._integrand, self.mmin, self.mmax)[0]
        return norm
    
        

