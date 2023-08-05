"""Spectral libraries and Broadband fluxes

Utility classes to manage collections of spectra. The main purpose of
this code is to compute effiently broadband fluxes from potentially
large series of SEDs.

Rationale
---------
When building broadband fluxes from spectra, it is efficient to first
project the spectra on a unique, well defined spline basis (generally
of low order, e.g.  1 or 2):

.. math:: S(\lambda) = \sum_i s_i B_i(\lambda) = B^T S

If the transmissions functions of the telescope are also developed on
a spline basis (not necessarily the same):

.. math:: T(\lambda) = \sum_i f_i K_i(\lambda) = K^T F

then, the broadband fluxes can be written as:

.. math:: \Phi= \int T(\lambda) \\frac{\lambda}{hc} S(\lambda) d\lambda = F^T G S

where :math:`G` is the *gramian* of the two bases, i.e.  the matrix
that contains the integrals of the dyadic products of the basis
elements: :math:`G_{ij} = \int B_i(x) K_j(x) dx`. Since the support of
the splines is finite, :math:`G` is a very sparse band-matrix, and the
computation of the integral above is very fast. In fact, the product
:math:`F^T G` can be precomputed and re-used for each spectrum, hence,
the integral reduces to a scalar product.

Stellar libs and Filter sets
----------------------------

A :class:`StellarLib`, such as :class:`Pickles` or :class:`Calspec`
contains a series of spectra, projected on a B-Spline basis (see e.g.
:class:`bspline.BSpline`).  The class holds an index, which
contains the metadata which happen to be available for each star (e.g.
spectral type, coordinates, ``V``-mag, ``B-V`` color etc.), as well as
a ndarray which contains the basis coefficients for all spectra.

The spectra may be loaded from the original files stored in
``SALTPATH`` and then projected on the basis.  For libraries of
moderate size such as Calspec or Pickles, this takes 1-2
seconds. Alternatively, the index and coefficient arrays may be saved
into a numpy ``.npz`` file (:meth:`StellarLib.save`) and later
reloaded from it (:meth:`StellarLib.load`) much faster, of course.

Examples
--------

Load the calspec library from the original files that are stored in
``SALTPATH``. Project the spectra on a order-2 (i.e. deg-1) BSpline
basis, defined on the range [3000, 12000] divided into 5\AA bins:

>>> import numpy as np
>>> from bspline import BSpline
>>> from . import stellarlibs
>>> grid = np.arange(3000., 12005., 5.)
>>> basis = BSpline(grid, order=2)
>>> calspec = stellarlibs.Calspec(basis=basis)

Save / load the basis into / from a .npz file

>>> calspec.save('calspec.npz')
>>> calspec = stellarlibs.Calspec(filename='calspec.npz')

Prepare a set of filters

>>> from .instruments import InstrumentModel
>>> grid = np.arange(3000., 12005., 10.)
>>> lsst = InstrumentModel("LSST")
>>> fs = stellarlibs.FilterSet(grid=grid, [lsst.EffectiveFilterByBand(b) for b in "griz"])

Compute broadband fluxes

>>> flx = stellarlibs.flux(calspec, fs)

Compute broadband mags

>>> m = stellarlibs.mag(calspec, fs, "AB")

Load the original spectra (no projections on a basis)

>>> index, spectra = stellarlibs.Pickles.fetch(basis=None)

Integrate the original spectra using Spectrum.IntegFlux

>>> flx = stellarlib.flux(spectra, fs)

Modify the atmosphere in the filter set

>>> from atmosphericmodel import Buton
>>> atm = Buton()
>>> fs.atmosphere = atm  # multiply by Buton and reproject the filters
>>> flx = stellarlib.flux(spectra, fs)

.. Warning:: IntegFlux and the gram() method (i.e.  the slow and
    fast options) should differ due to the infamous (hc)_snfit vs
    (hs)_scipy problem.  I am correcting the gram() flux by hand to
    adjust them to what IntegFlux returns. At some point, we need to
    correct both methods.
"""

import os
import os.path as op
#from exceptions import NotImplementedError, ValueError

import numpy as np
try:
    import pyfits as pf
except ImportError:
    import astropy.io.fits as pf
from .bspline import CardinalBSpline, BSpline, gram, lgram
from .spectrum import Spectrum, flambda_to_fclambda, CLIGHT_A_s, HPLANCK
from .instruments import MagSys
from . import constants
from ..util import saltpath, io

try:
    from sksparse.cholmod import cholesky_AAt
except ImportError:
    from scikits.sparse.cholmod import cholesky_AAt

# get rid of this at some point !
ALIGN_WITH_INTEG_FLUX = 0.9964833253040145 / 1.001899



class StellarLib(object):
    """Holds a collection of spectra projected on a spline basis.


    """
    def __init__(self, **kw):
        """Build the library, from a
        """
        if 'filename' in kw:
            self.load(kw['filename'])
        elif 'basis' in kw:
            self.basis = kw.pop('basis')
            self.grid = self.basis.grid
            self.index, self.fluxes = self.__class__.fetch(self.basis, **kw)
        elif 'grid' in kw:
            self.grid = self.pop('grid')
            self.basis = BSpline(self.grid)
            self.index, self.fluxes = self.__class__.fetch(self.basis, **kw)
        else:
            self.index, self.fluxes = self.__class__.fetch(None,**kw)

    def __len__(self):
        return len(self.index)

    def save(self, filename):
        """Save the stellar library contents into a .npz file

        Dump the basis, projected spectra and metadata into a single .npz file.

        Args:
            filename (str): name of the .npz file
        """
        np.savez(filename, grid=self.basis.grid, index=self.index, fluxes=self.fluxes)

    def load(self, filename):
        """Load the stellar library from a .npz filename.

        Load the basis, projected spectra, and spectrum metadata from
        the .npz file specified in argument.

        Args:
            filename (str): name of the .npz file
        """
        r = np.load(filename)
        self.grid = r['grid']
        self.basis = BSpline(self.grid)
        self.index = r['index']
        self.fluxes = r['fluxes']


class Pickles(StellarLib):
    """Spectra from (Pickles, 1992), projected on a BSpline basis.

    This is a specialization of :class:`StellarLib`, for the library
    of spectra described in (Pickles, 1992). This class implements
    essentially a method :meth:`load` which fetches the original
    spectra from their files, and projects them onto the basis
    specified by the user.
    """
    def __init__(self, **kw):
        """Constructor

        Instantiate the Pickles library.  This is not the original
        library in the sense that all the spectra are projected on a
        BSpline basis (of order 2, unless specified otherwise).

        Args:
            filename (str, optional): load the library from the file
            basis (BSpline, optional): specify the BSpline basis on
                which to project the spectra
            grid (ndarray, optional): specify the basis grid. An order 2
                (degree 1) BSpline basis will be instantiated on that grid.

        .. TODO
            add an option to self.load, so that it can retrieve the original
            (non projected) library.
        """
        super(Pickles, self).__init__(**kw)

    @staticmethod
    def fetch(basis):
        """fetch original spectra and project them on the spline basis

        Fetch the original spectra (from $SALTPATH/stellarlibs) and
        project them on the basis given in argument.

        Args:
            basis (BSpline type object): basis on which to project the spectra

        Returns:
            recarray, ndarray: index, spline coefficients if basis is not None
                               index, original spectra otherwise
        """
        import glob
        path = op.join(saltpath.stellar_libs_path, 'pickles')
        # retain only the 'u*.dat' spectra (extended)
        filenames = glob.glob(path + os.sep + 'u*.dat')
        #        filenames = filter(lambda x: op.basename(x)[0]!='u', filenames)
        n = len(filenames)

        # data structure
        # we separate the metadata (put in the index tab)
        # from the spline coefficients (stored in spectra)
        # it seems better to have the spline coeffs contiguous in memory.
        dtype = np.dtype([('styp', '|S10'),
                         ('filename', '|S20')])
        #                ('p', np.float64, len(basis))])
        index  = np.zeros(n, dtype=dtype)
        if basis is not None:
            spectra = np.zeros((n, len(basis)), dtype=np.float64)
            # we oversample a bit the spectra, to overconstrain
            # the basis projection a little
            gx = basis.grid
            ovsp_gx = np.hstack((gx, 0.5*(gx[1:]+gx[:-1])))
            ovsp_gx.sort()
        else:
            spectra = []

        # loop on the spectra
        for i,fn in enumerate(filenames):
            with open(fn) as f:
                wl, flux = [], []
                for line in f.readlines():
                    wl.append(float(line[0:7]))
                    flux.append(float(line[8:17]))
            wl, flux = np.asarray(wl), np.asarray(flux)
            index[i]['styp'] = op.basename(fn).split('.')[0]
            index[i]['filename'] = op.basename(fn)

            # oversample the spectral data and project it on the basis
            if basis is not None:
                yy = np.interp(ovsp_gx, wl, flux)
                spectra[i,:] = basis.linear_fit(ovsp_gx, yy)
            else:
                spectra.append(Spectrum(wl, flux))

        return index, spectra

class PicklesDepagne(StellarLib):
    """Spectra from (Pickles Depagne, 2010), projected on a BSpline basis.

    This is a specialization of :class:`StellarLib`, for the library
    of spectra described in (Pickles, 1992) plus a few peculiar
    types. The spectral types are matched to the tycho
    photometry. This class implements essentially a method
    :meth:`load` which fetches the original spectra from their files,
    and projects them onto the basis specified by the user.

    """
    def __init__(self, **kw):
        """Constructor

        Instantiate the library.  This is not the original library in
        the sense that all the spectra are projected on a BSpline
        basis (of order 2, unless specified otherwise), and have been
        renormalised to a synthetic mag VT=0.

        Args:
            filename (str, optional): load the library from the file
            basis (BSpline, optional): specify the BSpline basis on
                which to project the spectra
            grid (ndarray, optional): specify the basis grid. An order 2
                (degree 1) BSpline basis will be instantiated on that grid.
        """
        super(PicklesDepagne, self).__init__(**kw)

    @staticmethod
    def fetch(basis):
        """fetch original spectra and project them on the spline basis

        Fetch the original spectra (from $SALTPATH/stellarlibs) and
        project them on the basis given in argument.

        Args:
            basis (BSpline type object): basis on which to project the spectra

        Returns:
            recarray, ndarray: index, spline coefficients if basis is not None
                               index, original spectra otherwise
        """
        import glob
        path = op.join(saltpath.stellar_libs_path, 'picklesdepagne10')
        # retain only the 'u*.dat' spectra (extended)
        filenames = [op.join(path,  '%d.lib' % i) for i in range(141)]
        #        filenames = filter(lambda x: op.basename(x)[0]!='u', filenames)
        n = len(filenames)

        # data structure
        # we separate the metadata (put in the index tab)
        # from the spline coefficients (stored in spectra)
        # it seems better to have the spline coeffs contiguous in memory.
        dtype = np.dtype([('styp', '|S10'),
                         ('filename', '|S20')])
        #                ('p', np.float64, len(basis))])
        index  = np.zeros(n, dtype=dtype)
        if basis is not None:
            spectra = np.zeros((n, len(basis)), dtype=np.float64)
            # we oversample a bit the spectra, to overconstrain
            # the basis projection a little
            gx = basis.grid
            ovsp_gx = np.hstack((gx, 0.5*(gx[1:]+gx[:-1])))
            ovsp_gx.sort()
        else:
            spectra = []

        # loop on the spectra
        for i,fn in enumerate(filenames):
            nt = io.NTuple.fromtxt(fn)

            index[i]['styp'] = '%d' % i
            index[i]['filename'] = op.basename(fn)

            # oversample the spectral data and project it on the basis
            if basis is not None:
                yy = np.interp(ovsp_gx, nt['wl'], nt['flux'])
                spectra[i,:] = basis.linear_fit(ovsp_gx, yy)
            else:
                spectra.append(Spectrum(nt['wl'], nt['flux']))

        return index, spectra

class Calspec(StellarLib):
    """Spectra from the latest CALSPEC release (Bohlin, 2014),
    projected on a BSpline basis.

    This is a specialization of :class:`StellarLib`, for the library
    of spectra described in (Bohlin, 2014).
    """
    def __init__(self, **kw):
        super(Calspec, self).__init__(**kw)

    @staticmethod
    def fetch(basis, version='2015-01'):
        """load the spectra from the original files

        Args:
            basis (BSpline or None): BSpline basis to use
            version (str): CALSPEC release data

        Returns:
            recarray, ndarray: index and spline coeffs if basis is not None
                               index and list of Spectrum.Spectrum
        """
        path = op.join(saltpath.stellar_libs_path,
                       'calspec-' + version)
        # read the index
        index_file = op.join(path, 'index.org')
        if not op.isfile(index_file):
            raise ValueError('unable to find CALSPEC index: %s' % index_file)
        index = io.NTuple.fromorg(index_file)

        n = len(index)
        if basis is not None:
            gx = basis.grid
            ovsp_gx = np.hstack((gx, 0.5*(gx[1:]+gx[:-1])))
            ovsp_gx.sort()
            spectra = np.zeros((n, len(basis)), dtype=np.float64)
        else:
            spectra = []

        for i,d in enumerate(index):
            with pf.open(path + os.sep + d['FILENAME']) as f:
                wl = f[1].data['WAVELENGTH']
                flux = f[1].data['FLUX']
                if basis is not None:
                    #flux = flambda_to_fclambda(wl, flux)
                    yy = np.interp(ovsp_gx, wl, flux)
                    spectra[i,:] = basis.linear_fit(ovsp_gx, yy)
                else:
                    spectra.append(Spectrum(wl, flux))

        return index, spectra


class FilterSet(object):
    """
    Utility class that projects a set of filters on B-Splines
    and stores the projection coefficients.

    ..  note:: this code should be merged with
        :class:`instruments.FilterWheel`. We keep it here
        until we get to talk with the Great Guardians.
    """
    def __init__(self, basis, transmissions, atmosphere_model=None, distort_func=None):
        self.basis = basis
        if type(transmissions) is dict:
            self.transmissions = transmissions
        elif type(transmissions) is list:
            self.transmissions = dict([(t.InstrumentName + '::' + t.Band, t)
                                       for t in transmissions])
        # projection grid (larger than basis grid)
        self._grid, self._J, self._factor = self._projector(self.basis)
        self.atm = np.ones_like(self._grid)
        if distort_func is None:
            self.distort = None
        else:
            self.distort = distort_func(self._grid)
        self.parameters = self._project(basis, self.transmissions)
        self.bands = list(self.transmissions.keys())
        self.mean_wl = dict([(k,t.mean(t.x_min, t.x_max)) for k,t in list(self.transmissions.items())])

    def _projector(self, basis):
        # refine the basis grid
        gx = basis.grid
        gxx = np.hstack((gx, 0.5*(gx[1:]+gx[:-1])))
        gxx.sort()
        # precompute the projector
        # (will save repeated calls to cholesky_AAt)
        J = basis.eval(gxx).tocsr()
        factor = cholesky_AAt(J.T)
        return gxx, J, factor

    def _project(self, basis, transmissions):
        ret = {}
        if type(self.atm) is dict:
            # get rid of this case at some point.
            # this adds complications to the code
            # we do not need that anymore since
            # we now can extract a subset of the FilterSet
            for k,t in list(transmissions.items()):
                y = t(self._grid) * self.atm[k]
                if self.distort is not None:
                    y *= self.distort
                ret[k] = self._factor(self._J.T * y)
        else:
            for k,t in list(transmissions.items()):
                y = t(self._grid) * self.atm
                if self.distort is not None:
                    y *= self.distort
                ret[k] = self._factor(self._J.T * y)
        return ret

    def __len__(self):
        return len(self.transmissions)

    def __getitem__(self, key):
        return self.parameters[key]

    def extract(self, band_names):
        tr = [self.transmissions[b] for b in band_names]
        return FilterSet(self.basis, tr)

    def mean_wavelength(self, bandnames):
        d = self.mean_wl
        return np.asarray([d[bn] for bn in bandnames])

    @property
    def atmosphere(self):
        """return the current instance of the atmospheric transmission.

        The atmospheric transmission is stored as a grid vector, of
        size equal to that of the internal grid (self._grid). Return
        that vector.
        """
        return self.atm

    @atmosphere.setter
    def atmosphere(self, atmosphere_model):
        """change the current instance of the atmospheric transmission.

        Update the atmospheric transmission vector, and reproject the
        filters.

        Args:
            atmosphere_model (callable or dict of callables):
                 the function that defines the atmospheric transmission.
                 (possibly one different transmission per band)

        .. todo: add atmospheric transmission as an explicit parameter in self._project
        """
        if type(atmosphere_model) is dict:
            # get rid of this at some point
            self.atm = {}
            for k,f in list(atmosphere_model.items()):
                self.atm[k] = f(self._grid)
        else:
            self.atm = atmosphere_model(self._grid)
        self.parameters = self._project(self.basis, self.transmissions)

    @property
    def distortion(self):
        return self.distort

    @distortion.setter
    def distortion(self, distort_func):
        if distort_func is None:
            self.distort = None
        else:
            self.distort = distort_func(self._grid)
        self.parameters = self._project(self.basis, self.transmissions)


def flux(filters, splib, wl_step=5., z=0.):
    """Compute broadband fluxes (in e-/s)

    For each filter contained in the filter set, compute the the
    broadband fluxes of all the stars in the spectral library.

    The function follows the snfit convention, in the sense that it
    expects *rest frame* SED's, expressed in
    :math:`\mathrm{erg/cm^2/s/A}` and returns *observer frame*
    broadband fluxes expressed in :math:`e^-/s`.  The broadband flux
    is defined as:

    .. math:: f = \\frac{C}{(1+z)^2}\int S\\left(\\frac{\lambda}{1+z}\\right)\ \lambda\ T(\lambda)\ d\lambda

    where the integral is computed in the observer frame (hence the
    :math:`1/(1+z)^2` factor).  :math:`T` is the telescope
    transmission, in :math:`e^- cm^2 / \gamma`. The constant C is
    equal to :math:`1/hc` with h in erg s and c in A/s:

    .. math:: \\frac{1}{hc} \\approx 50341170.081942275\ \mathrm{erg^{-1} A^{-1}}

    using the values of h and c in `scipy.constants` (see however the
    warning section below).

    Args:
        splib (inherits from `StellarLib`): a spectral library, or at
            least an object that holds a basis as well as a set of
            coefficients.
        filters (`FilterSet`): a filter set
        wl_step (float, optional): integration step (if using
            traditional method)
        z (float): redshift to apply to the spectrum

    Returns:
        (numpy.rec.array) contains the broadband fluxes.

    .. note:: The function may be passed either a FilterWheel and a
         list of ``Spectra``, in which case it is going to
         call ``spectrum.IntegFlux`` on each spectrum.  Alternatively,
         we can pass it a ``stellarlibs.FilterSet`` and a
         ``stellarlibs.StellarLib``. In this case, it uses the faster
         Gram method (see above). To decide what to do, it the
         function checks whether splib and filters hold a bspline
         basis or not.

    .. WARNING:: IntegFlux and the gram() method (i.e.  the slow and
         fast options) differ due to the infamous (hc)_snfit vs
         (hs)_scipy problem.  I am correcting the gram() flux by hand
         to adjust them to what IntegFlux returns. At some point, we
         need to correct both methods.
    """
    names, fluxes = [], []

    if hasattr(splib, 'basis') and hasattr(filters, 'basis'):
        G = lgram(splib.basis, filters.basis, z=z)
        for key, pars in list(filters.parameters.items()):
            U = G.dot(pars)
            names.append(key)
            fluxes.append(ALIGN_WITH_INTEG_FLUX * np.dot(splib.fluxes, U))
    elif type(splib) is list:
        for k,tr in list(filters.transmissions.items()):
            names.append(k)
            fluxes.append([s.IntegFlux(tr, wavelength_integration_step=wl_step, z=z)
                           for s in splib])
    else:
        raise ValueError("don't know what to do with splib=%s" % splib.__class__)

    return np.rec.fromarrays(fluxes, names=names)


# from instruments import MagSys
# class MagSysFS(MagSys):

#     def __init__(self, magsys_name, basis=None):
#         super(MagSysFS, self).__init__(magsys_name)
#         if basis is None:
#             grid = np.arange(2000., 12000., 1.)
#             self.basis = BSpline(grid, order=4)
#         print self.pure_ab
#         if self.pure_ab:
#             x = np.arange(2000., 12000., 0.5)
#             self.spectrum = self.basis.linear_fit(x, constants.flux_ab(x))
#         else:
#             self.spectrum = self.

#     def ZeroPoint(self, fs):
#         pass

#     def mag(self, filterset, splib, z=0.):
#         pass


def mag(filters, splib, magsys, wl_step=5., z=0.):
    """Broadband mags of the stars in the spectral library.

    For each filter contained in the filter set, compute the the
    broadband magnitudes, in the specified magnitude system, of all
    the stars in the spectral library.

    Args:
        splib (inherits from `StellarLib`): spectral library
        filters (`FilterSet`): filters to use to compute the mags
        magsys (MagSys): magnitude system to use
        wl_step(float, optional): integration step (if using
            traditional method).
        z (float): redshift to apply to the spectrum

    Returns:
        (numpy.rec.array): contains the broadband magnitudes.
    """
    names, mags = [], []
    # fast option: splib and filters have a respline() method
    # that returns the basis and spline coefficients.
    # we can use the gram() method
    if hasattr(splib, 'basis') and hasattr(filters, 'basis'):
        G = lgram(splib.basis, filters.basis, z=z)
        for key, pars in list(filters.parameters.items()):
            T = filters.transmissions[key]
            zp = magsys.ZeroPoint(T)
            U = G.dot(pars)
            names.append(key)
            mags.append(-2.5 * np.log10(ALIGN_WITH_INTEG_FLUX * np.dot(splib.fluxes, U)) + zp)
    elif type(splib) is list:
        for key, tr in list(filters.transmissions.items()):
            names.append(key)
            T = filters.transmissions[key]
            zp = magsys.ZeroPoint(T)
            flx = np.asarray([s.IntegFlux(tr, wavelength_integration_step=wl_step)
                              for s in splib])
            mags.append(-2.5 * np.log10(flx) + zp)
    else:
        raise ValueError("don't know what to do with splib=%s" % splib.__class__)


    return np.rec.fromarrays(mags, names=names)

