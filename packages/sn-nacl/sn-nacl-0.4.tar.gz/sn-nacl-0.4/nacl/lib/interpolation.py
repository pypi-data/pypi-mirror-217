#!/usr/bin/python

""" Provides:
- Func1D: easy handling of tabulated 1D functions
"""

import numpy as np
from scipy import interpolate, integrate
import matplotlib.pyplot as plt
import sys


class Func1D(object):
    """ Wrapper around different ways of representing 1D function

    Func1D provides:
    - a callable interface to tabulated data (through 1D interpolation,
    - multiplication and addition of Func1D objects,
    - A routine for integration in a range.
    """
    def __init__(self, *func_like, **kwargs):
        """ Provide a Func1D interface over different data types

        Parameters:
        -----------
        func_like can be either:
            - a scalar
            - a callable (with only 1 parameter)
            - two arrays: in that case the function is an interpoltor of y = f(x) 
                          where x is the first array and y the second array


        It has an x_max and x_min member, that can either be set by options, 
        or that are the bounds of the x array. By default, they are both 0. 
        All this is made to be similar to snfit Sample1dFunction

        When 2 Func1D instances are multiplied x_min = max of the 2 x_min
        and x_max = min of the 2 x_max, like in sampledfunction.cc
        """
        self.x_min = 0
        self.x_max = 0

        if "x_min" in kwargs:
            self.x_min = kwargs["x_min"]
        if "x_max" in kwargs:
            self.x_max = kwargs["x_max"]

        if not "bounds_error"  in kwargs:
            bounds_error=False
        else:
            bounds_error = kwargs["bounds_error"]

        if len(func_like) > 2:
            raise ValueError("WARNING: Func1D can only deal with 1 or 2 args, not more")

        elif len(func_like) == 2:
            self.func = interpolate.interpolate.interp1d(
                func_like[0], func_like[1],
                bounds_error=bounds_error,
                fill_value=0)
            self.x_min = np.min(func_like[0])
            self.x_max = np.max(func_like[0])
        else:
            func_like = func_like[0]

            if isinstance(func_like, Func1D):
                self.func = func_like.func
            elif np.core.numeric.isscalar(func_like):
                self.func = lambda x: func_like
            elif callable(func_like):
                self.func = func_like
            else:
                raise ValueError("Don't know how to create a Func1D with what you provided, exiting")

    def __call__(self, x):
        """ 1D function evaluation at x.

        Parameter:
        ----------
        x: scalar or 1D array
        """
        return self.func(x)

    def __mul__(self, func2):
        """ Return a Func1D that will evaluate to the product of self
        and f2.
        """
        #- in this case, func2 would have default x_min and x_max 
        #- and 0 looses in the test just above
        x_min = self.x_min
        x_max = self.x_max

        if isinstance(func2, Func1D):
            x_min = max( self.x_min, func2.x_min )
            if func2.x_max != 0:
                x_max = min( self.x_max, func2.x_max )

        return Func1D( lambda x: self.func(x) * Func1D( func2 ).func(x), x_min=x_min, x_max=x_max )

    #- Func1D multiplication is commutative
    __rmul__ = __mul__

    def __div__(self, func2):
        """ Return a Func1D that will evaluate to the product of self
        and f2.
        """
        #- in this case, func2 would have default x_min and x_max 
        #- and 0 looses in the test just above
        x_min = self.x_min
        x_max = self.x_max

        if isinstance(func2, Func1D):
            x_min = max( self.x_min, func2.x_min )
            if func2.x_max != 0:
                x_max = min( self.x_max, func2.x_max )

        return Func1D( lambda x: self.func(x) / Func1D( func2 ).func(x), x_min=x_min, x_max=x_max )
    
    def __add__(self, func2):
        """ Return a Func1D that will evaluate to the sum of self
        and func2.
        """
        #- in this case, func2 would have default x_min and x_max 
        #- and 0 looses in the test just above
        x_min = self.x_min
        x_max = self.x_max

        if isinstance(func2, Func1D):
            x_min = max( self.x_min, func2.x_min )
            if func2.x_max != 0:
                x_max = min( self.x_max, func2.x_max )

        return Func1D( lambda x: self.func(x) + Func1D( func2 ).func(x), x_min=x_min, x_max=x_max )

    #- Func1D addition is commutative
    __radd__ = __add__


    def __sub__(self, func2):
        """ Return a Func1D that will evaluate to the difference of self
        and func2.
        """
        #- in this case, func2 would have default x_min and x_max 
        #- and 0 looses in the test just above
        x_min = self.x_min
        x_max = self.x_max

        if isinstance(func2, Func1D):
            x_min = max( self.x_min, func2.x_min )
            if func2.x_max != 0:
                x_max = min( self.x_max, func2.x_max )

        return Func1D( lambda x: self.func(x) - Func1D( func2 ).func(x), x_min=x_min, x_max=x_max )

    def __rsub__(self, func2):
        """ Return a Func1D that will evaluate to the difference of func2 and self

        func2 - self
        """
        #- in this case, func2 would have default x_min and x_max 
        #- and 0 looses in the test just above
        x_min = self.x_min
        x_max = self.x_max

        if isinstance(func2, Func1D):
            x_min = max( self.x_min, func2.x_min )
            if func2.x_max != 0:
                x_max = min( self.x_max, func2.x_max )

        return Func1D( lambda x: Func1D( func2 ).func(x) - self.func(x), x_min=x_min, x_max=x_max )

    
    def __pow__(self, func2):
        """ Return a Func1D that will evaluate to the self ** func2
        """
        #- in this case, func2 would have default x_min and x_max 
        #- and 0 looses in the test just above
        x_min = self.x_min
        x_max = self.x_max

        if isinstance(func2, Func1D):
            x_min = max( self.x_min, func2.x_min )
            if func2.x_max != 0:
                x_max = min( self.x_max, func2.x_max )

        return Func1D( lambda x:  self.func(x) ** (Func1D( func2 ).func(x)), x_min=x_min, x_max=x_max )

    def __rpow__(self, func2):
        """ Return a Func1D that will evaluate to the func2 ** self
        """
        #- in this case, func2 would have default x_min and x_max 
        #- and 0 looses in the test just above
        x_min = self.x_min
        x_max = self.x_max

        if isinstance(func2, Func1D):
            x_min = max( self.x_min, func2.x_min )
            if func2.x_max != 0:
                x_max = min( self.x_max, func2.x_max )

        return Func1D( lambda x: (Func1D( func2 ).func(x)) ** self.func(x), x_min=x_min, x_max=x_max )
    
    
    
    
    def integrate(self, range_inf, range_sup, method=100):
        """ Evaluate function integral in a range.

        Parameters:
        -----------
        range_inf: float
                   lower limit of the integration range
        range_sup: float
                   upper limit of the integration range
        method: can be either
              "romb": The integral is evaluated using the romberg method
              N (int): The integral is evaluated using a N points
                       simpson quadrature.
        """
        if isinstance(method, int):
            x = np.core.function_base.linspace(range_inf, range_sup, method)
#            return integrate.quadrature.simps(self(x), x=x)
            return integrate.simps(self(x), x=x)
        elif method == 'romb':
#            return integrate.quadrature.romberg(self, range_inf, range_sup)
            return integrate.romberg(self, range_inf, range_sup)

    def mean(self, range_inf=None, range_sup=None, method=100, order=0):
        """ Evaluate the mean using the function as a weight.

        Parameters:
        -----------
        range_inf: float
                   lower limit of the integration range
        range_sup: float
                   upper limit of the integration range
        method: to evaluate the integrals. Can be either:
              "romb": The integral is evaluated using the romberg method
              N (int): The integral is evaluated using a N points
                       simpson quadrature.
        """
        def identity(x):
            return x

        if range_inf is None:
            range_inf = self.x_min
        if range_sup is None:
            range_sup = self.x_max
        
        m = (self * identity).integrate(range_inf, range_sup, method=method)
        d = self.integrate(range_inf, range_sup, method=method)
        m /= d
        if order == 0:
            return m
        elif order == 1:
            def f(x):
                return np.abs(x - m)
        else:
            def f(x):
                return (x - m) ** order
        m2 = (self * f).integrate(range_inf, range_sup, method=method)
        return m2 / d

    def _x(self, x=None):
        if x is None:
            x = np.linspace(self.x_min, self.x_max, 100)
        return x
    
    def max(self, x=None):
        return self(self._x(x)).max()

    def min(self, x=None):
        return self(self._x(x)).min()
    
    def plot(self, start=None, stop=None, num=50, norm=False, scale=1.,  **keys):
        """ Plot the function in a range.

        Parameters:
        -----------
        start: The lower bound of the range.
        stop: The upper bound of the range.
        num: number of evaluation points in the range.
        norm: to normalize by the max value
        scale: to rescale the plot function

        All other keywords parameters are passed directly to plot.

        Example:
        --------
        >>> f = Func1D(np.sin)
        >>> f.plot(-np.pi, np.pi, 100, color='k')
        """
        if start is None:
            start = self.x_min
        if stop is None:
            stop = self.x_max
        x = np.core.function_base.linspace(start, stop, num)
        if norm:
            y = self(x) * scale
            return plt.plot(x, y / y.max(), **keys)
        else:
            return plt.plot(x, self(x) * scale, **keys)


if __name__ == "__main__":
    #- Implements few tests that I feel better if I can run from time to time

    x = Func1D(np.arange(1., 10., 0.1), np.arange(1., 10., 0.1))
    y = Func1D(np.arange(1., 10., 0.1), np.arange(1., 10., 0.1)+10.)
    

    print(("x(4.) + 1.    = %f     (should be 5.)" % ((x + 1.)(4.))))
    print(("1.    + x(4.) = %f     (should be 5.)" % ((1. + x)(4.))))

    print(("x(4.) - 1.    = %f     (should be 3.)" % ((x - 1.)(4.))))
    print(("1.    - x(4.) = %f     (shoudld be -3.)" % ((1. - x)(4.))))


    print(("x(4.) * 2.    = %f     (should be 8,)" % ((x * 2.)(4.))))
    print(("2.    * x(4.) = %f     (should be 8.)" % ((2. * x)(4.))))

    print(("x(4.) ** 2.    = %f     (should be 16,)" % ((x ** 2.)(4.))))
    print(("2.    ** x(4.) = %f     (should be 16.)" % ((2. ** x)(4.))))

    print(("(x + y)(2.)    = %f     (should be 14.)" % ((x + y)(2.))))
    print(("(y + x)(2.)    = %f     (should be 14.)" % ((y + x)(2.))))
    print(("(x * y)(2.)    = %f     (should be 24.)" % ((x * y)(2.))))
    print(("(y * x)(2.)    = %f     (should be 24.)" % ((y * x)(2.))))
    print(("(x ** y)(2.)   = %f     (should be 4096.)" % ((x ** y)(2.))))
    print(("(y ** x)(2.)   = %f     (should be 144.)" % ((y ** x)(2.))))    
    

    
