"""
The SALT2 model. 

SALT2 parameterizes the *restframe* spectrophotometric evolution of
SNe Ia with two surfaces and a color law:

.. math:: S_{10}(p, \lambda) = X_0 \\left(M_0(p, \lambda) + X_1 M_1(p,\lambda)\\right) C(\lambda)

Given a passband, :math:`T(\lambda)`, the model allows one to compute
an *observer frame* broadband flux:

.. math:: f = \\frac{C\ 10^{-12}}{1+z} \int S_{10}\\left(p, \\frac{\lambda}{1+z}\\right)\ \lambda\ T(\lambda)\ d\lambda

"""

import os
import os.path as op
import sys 
import re

import numpy as np 
from scipy.sparse import coo_matrix

from ..util.io import NTuple
from ..lib.stellarlibs import FilterSet, ALIGN_WITH_INTEG_FLUX
from ..lib.instruments import InstrumentModel 
from ..lib.fitparameters import FitParameters
from ..lib.bspline import BSpline, BSpline2D, lgram
from . import saltpath


def load_filters(bands):
    """
    Load all the filters that are requested in argument and return a
    FilterSet
    
    .. note :: this function is currently slow, because no instrument
               cache implemented.
    """
    instrument_names = np.unique([re.search('(.+)::(.+)', bn).group(1) for bn in bands])
    instruments = [InstrumentModel(nm) for nm in instrument_names]
    instruments = dict(list(zip(instrument_names, instruments)))
    tr, lmin, lmax = [], [], []
    for bn in bands:
        instr, band = re.search('(.+)::(.+)', bn).groups()
        f = instruments[instr].EffectiveFilterByBand(band)
        lmin.append(f.x_min)
        lmax.append(f.x_max)
        tr.append(f)
    gwl = np.arange(min(2000., np.min(lmin)), 
                    max(11000., np.max(lmax)), 5.)
    basis = BSpline(gwl, order=2)
    return FilterSet(basis, tr)


class ModelComponents(object):
    """Basic ingredients of the SALT2 model
    
    Holds all the model ingredients that are shared between all supernovae:
      - model validity area in phase and wavelength
      - BSpline basis definitions
      - surfaces
      - color law
      - error snakes
      - color smearing laws
    """
    def __init__(self, filename=None):
        self.basis, self.wl_basis, self.phase_basis = None, None, None
        self.M0, self.M1 = None, None
        self.cl = None
        if filename is not None:
            self.load(filename)

    def save(self, filename):
        if self.basis is None:
            return 
        np.savez(filename, 
                 wl_grid=self.wl_basis.grid,
                 phase_grid=self.phase_basis.grid, 
                 M0=self.M0, 
                 M1=self.M1, 
                 CL_pars=self.cl.pars, 
                 CL_range=[self.cl.min_lambda, self.cl.max_lambda])
    
    def load(self, filename):
        arrs = np.load(filename)
        wl_grid, phase_grid = arrs['wl_grid'], arrs['phase_grid']
        self.basis = BSpline2D(wl_grid, phase_grid, x_order=4, y_order=4)
        self.wl_basis = self.basis.bx
        self.phase_basis = self.basis.by
        self.M0, self.M1 = arrs['M0'], arrs['M1']
        self.cl = ColorLaw(arrs['CL_pars'], arrs['CL_range'])

    @staticmethod
    def load_from_saltpath():
        """load the SALT2 model from an "official" SALT2 repository
        """

        phase_grid = np.linspace(-20., 51., 50)
        wl_grid    = np.linspace(2000., 9201., 300)
        basis      = BSpline2D(phase_grid, wl_grid, x_order=4, y_order=4)
        
        cfg = saltpath.read_card_file(saltpath.fitmodel_filename)
        salt2_model_path = saltpath.SALTPATH + os.sep + cfg['SALT2']
    
        # first surface
        M0_filename = salt2_model_path + os.sep + 'salt2_template_0.dat'
        d = NTuple.fromtxt(M0_filename)
        phase, wl, flx = d['f0'].copy(), d['f1'].copy(), d['f2'].copy()
        M0 = basis.linear_fit(phase, wl, flx)
    
        # second surface 
        M1_filename = salt2_model_path + os.sep + 'salt2_template_1.dat'
        d = NTuple.fromtxt(M1_filename)
        phase, wl, flx = d['f0'].copy(), d['f1'].copy(), d['f2'].copy()
        M1 = basis.linear_fit(phase, wl, flx)
    
        # color law 
        print((salt2_model_path + os.sep + 'salt2_color_correction.dat'))
        cl_filename = salt2_model_path + os.sep + 'salt2_color_correction.dat'
        with open(cl_filename) as f:
            deg = int(f.readline())
            p = []
            for i in range(deg):
                p.append(float(f.readline()))
            r = {}
            for line in f:
                field, value = re.search('^Salt2ExtinctionLaw\.([\w_]+)\s*([\d\.+-]+)', line).groups()
                r[field] = float(value)
            assert 'version' in r and r['version'] == 1.0
        
        ret = ModelComponents()
        ret.basis = basis
        ret.phase_basis = basis.bx
        ret.wl_basis = basis.by
        ret.M0 = M0.reshape(len(ret.wl_basis), -1)
        ret.M1 = M1.reshape(len(ret.wl_basis), -1)
        alpha = 1. - np.sum(p)
        p = np.asarray(p[::-1] + [alpha])
        ret.cl = ColorLaw(p, (r['min_lambda'], r['max_lambda']))
        ret.CC = ret.cl(ret.wl_basis.grid, 1.)
        return ret


class ColorLaw(object):
    """Implementation of the SALT2 color law (version 1)
    
    The SALT2 color law describes the color diversity of SNeIa. It is
    fitted from a training sample. In SALT 2.4, the color law is
    parametrized as follows:
    
    .. math:: C(\lambda;c) = 10^{0.4 (c \times P(\lambda))}

    where :math:`P(\lambda)` is a polynomial, such as
    :math:`P(\lambda_B) = 1` and :math:`P(\lambda_V) = 0` It is
    defined in the wavelength range :math:`2800 A < \lambda < 7000 A`
    """
    WAVELENGTH = {"U": 3650.88, "B": 4302.57, "V": 5428.55, "R": 6418.01, "I": 7968.34}
    U_WAVELENGTH=3650.88
    B_WAVELENGTH=4302.57
    V_WAVELENGTH=5428.55
    R_WAVELENGTH=6418.01
    I_WAVELENGTH=7968.34
    
    def __init__(self, pars, wl_range):
        """Constructor - computes the arguments 
        
        """
        assert(wl_range[0] < wl_range[1])
        self.min_lambda, self.max_lambda = wl_range
        
        self.pars = pars
        
        self.min_reduced_lambda = self.reduce(self.min_lambda)
        self.max_reduced_lambda = self.reduce(self.max_lambda)
        
        dpars = np.polyder(self.pars)
        
        # uv side 
        val = np.polyval(self.pars, self.min_reduced_lambda)
        dval = np.polyval(dpars, self.min_reduced_lambda)
        self.pars_uv = np.asarray([dval * self.min_reduced_lambda + val,
                                   val * self.min_reduced_lambda])
        # ir side 
        val = np.polyval(self.pars, self.max_reduced_lambda)
        dval = np.polyval(dpars, self.max_reduced_lambda)
        self.pars_ir = np.asarray([dval * self.max_reduced_lambda + val,
                                   val * self.max_reduced_lambda])
        
    def reduce(self, wl):
        B_WL, V_WL = self.WAVELENGTH["B"], self.WAVELENGTH["V"]
        return (wl-B_WL)/(V_WL-B_WL);
    
    def __call__(self, wl, color):
        rwl = self.reduce(np.asarray(wl))
        r = np.polyval(self.pars, rwl) * rwl
        idx_uv = rwl<self.min_reduced_lambda
        r[idx_uv] = np.polyval(self.pars_uv, rwl[idx_uv]-self.min_reduced_lambda)
        idx_ir = rwl>self.max_reduced_lambda
        r[idx_ir] = np.polyval(self.pars_ir, rwl[idx_ir]-self.max_reduced_lambda)
        return np.power(10., 0.4 * color * r)


def precompute_filter_effective_restframe_lambda(model, fs, zgrid):
    """re
    """
    def effective_lambda(model, fs, z):
        """
        Compute 
        \int \lambda^2 B_i(\lambda) B_j(\lambda (1+z)) d\lambda / \int \lambda B_i B_j d\lambda
        """
        G  = coo_matrix(lgram(model.wl_basis, fs.basis, z=z))
        G2 = coo_matrix(lgram(model.wl_basis, fs.basis, z=z, lambda_power=2))
        assert ~np.any(G.row-G2.row) and ~np.any(G.col-G2.col)
        leff = G2.data/G.data
        L = coo_matrix((leff, (G.row, G.col)), shape=G.shape)
        N = coo_matrix((np.ones_like(leff), (G.row, G.col)), shape=G.shape)
        leff = np.array(L.sum(axis=1)).squeeze()
        N = np.array(N.sum(axis=1)).squeeze()
        idx = N>0
        leff[idx] /= N[idx]
        return leff
        
    #    self.CC = self.model.cl(self.leff / (1.+self.z), 1.)
    #    self.CC[~idx] = 1.
    leff = []
    # refine the z_grid
    for z in zgrid:
        leff.append(effective_lambda(model, fs, z))
        print((z, leff[-1][0], leff[-1][-1]))
    leff = np.vstack(leff)
    bs = BSpline2D(model.wl_basis.grid, zgrid, x_order=1, y_order=1)
    X,Y = np.meshgrid(model.wl_basis.grid, zgrid)
    
    return bs, X.flatten(), Y.flatten(), leff


    
def param_setter(name):
    def set_param(self, val):
        self.pars[name] = val
    return set_param


def param_getter(name):
    def get_param(self):
        return self.pars[name].full[0]
    return get_param


class SALT2(object):
    """Evaluate the SALT2 model for a specific supernova

    An instance of this class takes as an input a list of observations
    (MJDs, bands).  It precomputes and caches everything that can be
    pre-computed, essentially, the color law, the gram at that
    redshift and the Gram folded with the passband coefficients.  

    When __call__'ed with a parameter vector, it evaluates the SALT2
    model for each observation.
    
    """
    def __init__(self, mjds, bands, model, filterset, z=0., wl_range=(3000., 8000.)):
        """Constructor

        Stores the list of observations, initialize a parameter vector, 
        
        """
        # basic stuff 
        self.mjds = mjds
        self.bands = bands
        #        self.bands_unique, self.band_index =
        self.build_band_index(bands)
        self.model = model
        # assumes filterset has all bands that are needed
        self.filterset = filterset
        # expect M0 and M1 to be matrices
        self.M0, self.M1 = model.M0, model.M1
        self.restframe_wavelength_range = wl_range
        
        # set up an internal parameter vector 
        self.pars = self.init_pars()
        
        # set the redshift. This triggers a recompute 
        # of the Gram and Fz matrices and the color law
        self.z = z
        
    # properties, for easy access to the internal parameter vector (somewhat slow)
    X0 = property(fget=param_getter('X0'), fset=param_setter('X0'))
    X1 = property(fget=param_getter('X1'), fset=param_setter('X1'))
    Color = property(fget=param_getter('Color'), fset=param_setter('Color'))
    DayMax = property(fget=param_getter('DayMax'), fset=param_setter('DayMax'))

    # special property for z, because when we change z, 
    # we have to recompute the grams and the color law...
    @property
    def z(self):
        return self.pars['z'].full[0]
    @z.setter
    def z(self, val):
        self.pars['z'] = val
        self.G, self.Fz = self.init_fz()
        self.init_CC()

    def build_band_index(self, bands):
        self.bands_unique = np.unique(bands)
        idx = dict(list(zip(self.bands_unique, np.arange(len(self.bands_unique)))))
        self.band_index = np.array([idx[b] for b in bands])
        return self.bands_unique, self.band_index        
        
    def init_fz(self):
        """creates and return the F(z) matrix
        """
        G = lgram(self.model.wl_basis, self.filterset.basis, z=self.z)
        Fz = np.vstack([G * self.filterset[b] for b in self.bands_unique])
        return G, Fz
    
    def init_CC(self):
        """evaluate the color law
        """
        if not hasattr(self, 'G'):
            self.G = lgram(self.model.wl_basis, self.filterset.basis, z=self.z)
        G = coo_matrix(self.G)
        self.G2 = lgram(self.model.wl_basis, self.filterset.basis, z=self.z, lambda_power=2)
        G2 = coo_matrix(self.G2)
        assert ~np.any(G.row-G2.row) and ~np.any(G.col-G2.col)
        leff = G2.data/G.data
        L = self.L = coo_matrix((leff, (G.row, G.col)), shape=G.shape)
        N = self.N = coo_matrix((np.ones_like(leff), (G.row, G.col)), shape=G.shape)
        self.leff = np.array(L.sum(axis=1)).squeeze()
        N = np.array(N.sum(axis=1)).squeeze()
        idx = N>0
        self.leff[idx] /= N[idx]
        self.CC = self.model.cl(self.leff / (1.+self.z), 1.)
        self.CC[~idx] = 1.

    def mask_forbidden_bands(self):
        """evaluate the mask
        """
        mean_restframe_wavelength = self.filterset.mean_wavelength(self.bands) / (1.+ self.z)
        blue_cutoff, red_cutoff = self.restframe_wavelength_range
        return (mean_restframe_wavelength>blue_cutoff) & (mean_restframe_wavelength<red_cutoff)
        
    @staticmethod
    def init_pars():
        p = FitParameters([('X0', 1), ('X1', 1), ('Color', 1), ('DayMax', 1), ('z', 1)])
        p['X0'] = 1.
        p['X1'] = 0.
        p['Color'] = 0.
        p['DayMax'] = 0.
        p['z'] = 0.
        p.fix('z')
        return p
    
    def __call__(self, p=None, jac=False):
        """evaluate the model and its derivatives (optional)
        
        The broadband flux is given by:

        .. math:: F(p) = X_0 \times \\left(I_0 + X_1 I_1\\right)) \\times  10^{0.4 c P(\lambda)}
        """
        if p is not None:
            self.pars.free = p 
        M0, M1, Fz = self.M0, self.M1, self.Fz
        z, X0, X1, Color, DayMax = self.z, self.X0, self.X1, self.Color, self.DayMax
        
        phase = (self.mjds-DayMax) / (1. + self.z)

        # using a sparse csc() makes a noticeable difference
        # (x4 in speed with respect to multiply dense matrices)
        # even in the other matrix (M0, M1) is dense
        # (M0, M1 has to be a matrix though, not an array)
        # 
        # *TODO*: understand what underlying function is called
        # 
        P = self.model.phase_basis.eval(phase).tocsc()
        CC = np.power(self.CC, Color)
        M0_CC  = np.matrix(self.M0.T * CC)
        M1_CC  = np.matrix(self.M1.T * CC)
        Fz = Fz[self.band_index]
        I0 = (np.array(P * M0_CC) * Fz).sum(axis=1)
        I1 = (np.array(P * M1_CC) * Fz).sum(axis=1)
        
        # OLD version 
        #        # seems to be much faster with dense matrices
        #        P = self.model.phase_basis.eval(phase).todense()
        #        CC = np.power(self.CC, Color)
        #        I0 = (np.array(P * (M0.T * CC)) * Fz).sum(axis=1)
        #        I1 = (np.array(P * (M1.T * CC)) * Fz).sum(axis=1)        
        
        # I add the (1+z) factor and the ALIGN_WITH_INTEG_FLUX here
        norm = 1.E-12 * (1.+z) * ALIGN_WITH_INTEG_FLUX
        flux = norm * X0 * (I0 + X1*I1)
        
        # no derivatives ? just return the model value 
        if not jac:
            return flux
        
        # compute the derivatives w.r.t. parameters 
        n, N = len(self.pars.free), len(phase)
        J = np.zeros((N,n))
        
        # ddX0
        i = self.pars['X0'].indexof(0)
        if i>=0:
            J[:, i] = norm * (I0 + X1*I1)
            
        # ddX1
        i = self.pars['X1'].indexof(0)
        if i>=0:
            J[:, i] = norm * (X0 * I1)
        
        # ddDayMax 
        i = self.pars['DayMax'].indexof(0)
        if i>=0:
            #            dP = self.model.phase_basis.deriv(phase).todense() * (-1. / (1.+z))
            dP = self.model.phase_basis.deriv(phase)
            dP.data *= (-1. / (1.+z))
            dP = dP.tocsc()
            dI0 = (np.array(dP * M0_CC) * Fz).sum(axis=1)
            dI1 = (np.array(dP * M0_CC) * Fz).sum(axis=1)
            J[:, i] = norm * X0 * (dI0 + X1 * dI1)
        
        # ddColor 
        i = self.pars['Color'].indexof(0)
        if i>=0:
            dCC = np.log(self.CC) * CC
            M0_dCC, M1_dCC = np.matrix(M0.T * dCC), np.matrix(M1.T * dCC)
            dI0 = (np.array(P * M0_dCC) * Fz).sum(axis=1)
            dI1 = (np.array(P * M1_dCC) * Fz).sum(axis=1)
            J[:, i] = norm * X0 * (dI0 + X1 * dI1)
        
        # ddz - this one is costly to compute
        # I don't know how to compute it other than numerically
        i = self.pars['z'].indexof(0)
        if i>=0:
            self.z += dz
            dflux = self()
            J[:,i] = (dflux-flux)/dz
            self.z -= dz
        
        return flux, J
    
    def deriv_debug(self, p=None):
        if p is not None:
            self.pars.free = p 
        
        flx0 = self(jac=0)

        n, N = len(self.pars.free), len(self.mjds)
        J = np.zeros((N,n))        
        
        # ddX0
        self.X0 += 0.01
        flx = self()
        J[:, self.pars['X0'].indexof(0)] = (flx-flx0) / 0.01
        self.X0 -= 0.01
        # ddX1
        self.X1 += 0.01
        flx = self()
        J[:, self.pars['X1'].indexof(0)] = (flx-flx0) / 0.01
        self.X1 -= 0.01
        # ddDayMax 
        self.DayMax += 0.01
        flx = self()
        J[:, self.pars['DayMax'].indexof(0)] = (flx-flx0) / 0.01
        self.DayMax -= 0.01        
        # ddColor 
        self.Color += 0.001
        flx = self()
        J[:, self.pars['Color'].indexof(0)] = (flx-flx0) / 0.001
        self.Color -= 0.001      
        # ddz
        self.z += 0.1
        flx = self()
        J[:, self.pars['z'].indexof(0)] = (flx-flx0) / 0.01
        self.z -= 0.1

        return J 
        
def test():
    r = []
    for sn in sne:
        r.append(SALT2(sn))




