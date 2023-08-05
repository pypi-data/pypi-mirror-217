#!/usr/bin/python

####
# Re-implementation of the original SALT2 model.
####

import logging
import time

import numpy as np
import scipy.sparse

try:
    from sksparse.cholmod import cholesky_AAt
except ImportError:
    from scikits.sparse.cholmod import cholesky_AAt

from ..instruments import FilterDb
from ..lib import bspline
from ..lib.fitparameters import FitParameters
from ..lib.instruments import MagSys
from . import variancemodels as vm

from nacl.dataset import SimTrainingDataset


logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.INFO)


class ColorLaw:
    r"""Implementation of the SALT2 color law (version 1)

        The SALT2 color law describes the color diversity of SNeIa. In SALT 2.4, the
        color law is parametrized as follows:

        .. math::
            CL(\lambda;c) = 10^{0.4\ c \times P(\lambda_r)}

        where :math:`P(\lambda_r)` is a polynomial, such as :math:`P(\lambda_B) = 0`
        and :math:`P(\lambda_V) = 1`.

        This implies the following transformation :

        .. math::
            \lambda_r = \frac{\lambda-\lambda^B}{\lambda^V - \lambda^B}

        It is defined in the wavelength range :math:`2800 A < \lambda < 7000 A` and
        extrapolated with a linear function outside this interval.

        This class evaluates :math:`P(\lambda, \alpha_i)` and its derivatives
        :math:`\partial P/\partial \alpha_i` (which is the painful part).

        Attributes
        ----------
        min_lambda : float
            Lower value of the wavelength interval
        max_lambda : float
            Upper value of the wavelength interval
        min_reduced_lambda : float
            Lower value of the reduce wavelength interval
        max_reduced_lambda : float
            Upper value of the reduce wavelength interval
        pars : array
            Color law polynomial parameters
        pars_ir :
            Parameters of the IR affine extension
        pars_uv
            Parameters of the UV affine extension
    """
    WAVELENGTH = {"U": 3650.88, "B": 4302.57, "V": 5428.55, "R": 6418.01, "I": 7968.34}
    U_WAVELENGTH = 3650.88
    B_WAVELENGTH = 4302.57
    V_WAVELENGTH = 5428.55
    R_WAVELENGTH = 6418.01
    I_WAVELENGTH = 7968.34

    def __init__(self, wl_range=[2800, 7000]):
        """
            Constructor - computes the arguments

            Parameters
            ----------
            wl_range : list or ndarray
                nominal wavelength range for the polynom color law.
                Outside this range, we don't expect to have valid data
                and the color law is extrapolated with deg-1 polynomials.
        """
        assert (wl_range[0] < wl_range[1])
        self.min_lambda, self.max_lambda = wl_range

        self.min_reduced_lambda = self.reduce(self.min_lambda)
        self.max_reduced_lambda = self.reduce(self.max_lambda)
        self.pars = np.zeros(5)

    def reduce(self, wl):
        r"""Linear remapping of the wavelength passed in argument.

            The remapping is defined by:

            .. math::
                \lambda_r = \frac{\lambda - \lambda_B}{\lambda_V - \lambda_B}

            Parameters
            ----------
            wl : array-like
                the input wavelengths in Angstroms

            Returns
            ----------
            array of floats
                the reduced wavelengths
        """
        B_WL, V_WL = self.WAVELENGTH["B"], self.WAVELENGTH["V"]
        return (wl-B_WL)/(V_WL-B_WL)

    def __call__(self, wl, p, jac=False):  # return_jacobian_as_coo_matrix=False):
        r"""Evaluate the polynomial part of the color law

            The full SALT2 color law is given by:

            .. math::
                CL(\lambda, c) = 10^{0.4\ c\ P(\lambda, \alpha_i)}

            with

            .. math::
                P(\lambda) = \left\{ \begin{split}
                P'(\bar\lambda_{UV}) \times (\bar\lambda-\bar\lambda_{UV}) + P(\bar\lambda_{UV})
                & \ \ \ \ \mathrm{if \lambda < \lambda_{UV}} \\
                \bar\lambda \times \left(\sum_{i=1}^4 \alpha_i \bar\lambda^i + 1 - \sum_{i=1}^4\alpha_i\right)
                & \ \ \ \ \mathrm{if \lambda_{UV} < \lambda < \lambda_{IR}} \\
                P'(\bar\lambda_{IR}) \times (\bar\lambda-\bar\lambda_{IR}) + P(\bar\lambda_{IR})
                & \ \ \ \ \mathrm{if \lambda > \lambda_{IR}} \\
                \end{split}\right.

            and :math:`\lambda_r` defined above.

            This function evaluates :math:`P(\lambda,\alpha_i)` along with its derivatives w.r.t. the :math:`\alpha_i`:
            :math:`\partial P/\partial \alpha_i`

            Parameters
            ----------
            wl : ndarray of float
                input wavelengths (in Angstroms)
            p : ndarray
                color law parameters (i.e. the :math:`(\alpha_i)_{1\leq i \leq 4}`)
            jac : bool (default=False)
                whether to return the jacobian matrix
            return_jacobian_as_coo_matrix : bool
                If jacobian needs to be scipy.sparse

            Returns
            ----------
            cl : array-like of float
                the color law values
            jacobian : numpy.array or scipy.sparse.csr_matrix (return_jacobian_as_coo_matrix)
                the matrix of derivatives, if `jac` is True
        """
        self.pars[0:4] = p
        self.pars[4] = 1 - p.sum()
        d_pars = np.polyder(self.pars)

        # nominal range
        rwl = self.reduce(np.asarray(wl))
        r = np.polyval(self.pars, rwl) * rwl

        # uv side (if necessary)
        idx_uv = rwl < self.min_reduced_lambda
        has_uv_data = idx_uv.sum() > 0
        if has_uv_data:
            val = np.polyval(self.pars, self.min_reduced_lambda)
            d_val = np.polyval(d_pars, self.min_reduced_lambda)
            self.pars_uv = np.asarray([d_val * self.min_reduced_lambda + val,
                                       val * self.min_reduced_lambda])
            r[idx_uv] = np.polyval(self.pars_uv, rwl[idx_uv]-self.min_reduced_lambda)

        # ir side
        idx_ir = rwl > self.max_reduced_lambda
        has_ir_data = idx_ir.sum() > 0
        if has_ir_data:
            val = np.polyval(self.pars, self.max_reduced_lambda)
            d_val = np.polyval(d_pars, self.max_reduced_lambda)
            self.pars_ir = np.asarray([d_val * self.max_reduced_lambda + val,
                                       val * self.max_reduced_lambda])
            r[idx_ir] = np.polyval(self.pars_ir, rwl[idx_ir]-self.max_reduced_lambda)

        if not jac:
            return r, None

        # the jacobian is unfortunately a dense matrix
        # (maybe we should try using splines)
        #
        # In the nominal wavelength range, it has the form:
        #
        #   [l_1**5-l_1   l_1**4-l1    l_1**3-l1  l_1**2-l1]
        #   [  ...          ...           ...       ...    ]
        #   [l_N**5-l_1   l_N**4-l1    l_N**3-l1  l_N**2-l1]
        #
        v = np.vander(rwl, 6)[:, 0:-2]
        jacobian = (v.T-rwl).T

        #
        # and in the extrapolation range, it has the form:
        #
        # J_ik = [dCL'/da_k(rwl-rwl_uv) + dCL/da_k]
        #
        # Granted, it's not very readable. But it should be fast enough
        if has_uv_data:
            l_uv = self.min_reduced_lambda
            j1_luv = (np.vander([l_uv], 6)[:, 0:-2].T - np.array([l_uv])).T
            j2_luv = np.vander([l_uv], 5)[:, 0:-1] * np.array([5., 4., 3., 2.]) - 1.
            n_uv = idx_uv.sum()
            jacobian[idx_uv] = j2_luv * (rwl[idx_uv]-l_uv).reshape(n_uv, -1) + j1_luv * np.ones(n_uv).reshape(n_uv, -1)

        if has_ir_data:
            l_ir = self.max_reduced_lambda
            j1_lir = (np.vander([l_ir], 6)[:, 0:-2].T - np.array([l_ir])).T
            j2_lir = np.vander([l_ir], 5)[:, 0:-1] * np.array([5., 4., 3., 2.]) - 1.
            n_ir = idx_ir.sum()
            jacobian[idx_ir] = j2_lir * (rwl[idx_ir]-l_ir).reshape(n_ir, -1) + j1_lir * np.ones(n_ir).reshape(n_ir, -1)

        # check for nan's and inf's
        if np.any(np.isnan(r)) or np.any(np.isinf(r)):
            raise ValueError('inf/nan values in color law')

        #
        # if return_jacobian_as_coo_matrix:
        #    jacobian = scipy.sparse.coo_matrix(jacobian)

        return r, jacobian


class SpectrumRecalibrationPolynomials:
    r"""A class to manage the spectrum recalibration polynomials
        The photometric calibration of spectra is generally affected by significant
        error modes at large wavelength scales.
        It is imperative to remove these error modes, while preserving the information provided by
        the spectra at small scales (spectral features)

        This is achieved during training by multiplying the spectral predictions of the model by a
        recalibration polynomial specific to each spectrum, function of the observation
        wavelength :math:`\lambda_o`, and of order :math:`N_s = 3`, common to all spectra:

        .. math::

            s(\lambda_{rec}) = \sum_i^{N_s} s_i \lambda_{rec}^{N_s - i} %quad \mbox{and}
            \quad \lambda_{0} = \frac{\lambda - 5000}{9000 - 2700}

        with:

        .. math::
            \lambda_{rec} = \frac{2 (\lambda_o - \lambda_{max})}{\lambda_{max} - \lambda_{min}+1

        Attributes
        ----------
        tds : nacl.dataset.TrainingDataset
            Data set of photometric and spectroscopic observations.
        model : nacl.model.salt
            Model.
        pol_degrees : int or indexable structure
            Polynomial degree for each spectrum.
        N : int
            Number of spectral data point.
        offset : numpy.array
            Starting point of parameter index for each spectrum.
        n : int
            Number of recalibration parameters
        jacobian : scipy.sparse.coo_matrix
            Jacobian matrix of the recalibration polynomial functions.
    """

    def __init__(self, tds, model, pol_degrees):
        """Constructor

           Parameters
           ----------
            tds : nacl.dataset.TrainingDataset
                Data set of photometric and spectroscopic observations.
            model : nacl.model.salt
                Model.
            pol_degrees : int or indexable structure
                Polynomial degree for each spectrum.
            """
        self.tds = tds
        self.model = model
        self.pol_degrees = pol_degrees
        self.jacobian = None

        self.N = len(self.tds.spec_data)
        o = np.cumsum(np.hstack(([0], self.pol_degrees+1)))
        self.offset, self.n = o[:-1], o[-1]
        self.build_jacobian_matrix()

    def init_pars(self):
        """return a parameter vector initialized such that
            the recalibration polynomials are evaluated to 1
            for each spectra.

            Returns
            -------
            array
                Initiated parameters.
        """
        p = np.zeros(self.n)
        o = np.cumsum(self.pol_degrees+1) - 1
        p[o] = 1.
        return p

    def build_jacobian_matrix(self):
        """
            Create the jacobian matrix where line correspond to all spectral data point and
            the colones to parameters.
            """
        i, j, v = [], [], []

        # easier to write this with the spectra index
        for sp in self.tds.spectra:
            spec_index = sp.spec_index[0]
            lmin, lmax = sp.wavelength.min(), sp.wavelength.max()
            a = 2. / (lmax-lmin)
            b = 1 - 2. * lmax / (lmax-lmin)
            rwl = a * sp.wavelength + b
            deg = self.pol_degrees[spec_index]
            jacobian_spec_rec = scipy.sparse.coo_matrix(np.vander(rwl, deg+1))
            i.append(jacobian_spec_rec.row + sp.slc.start)
            j.append(jacobian_spec_rec.col + self.offset[spec_index])
            v.append(jacobian_spec_rec.data)
        i = np.hstack(i)
        j = np.hstack(j)
        v = np.hstack(v)
        self.jacobian = scipy.sparse.coo_matrix((v, (i, j)), shape=(self.N, self.n)).tocsr()

        # for isp in range(self.tds.nb_spectra()):
        #     # for sp in self.tds.spectra:
        #     idx_sp = self.tds.spec_data.spec_index == isp
        #     sp = self.tds.spec_data[idx_sp]
        #     sli = np.where(idx_sp)[0]
        #     slc = slice(sli.min(), sli.max()+1)

        #     lmin, lmax = sp['wavelength'].min(), sp['wavelength'].max()
        #     a = 2. / (lmax-lmin)
        #     b = 1 - 2. * lmax / (lmax-lmin)
        #     rwl = a * sp['wavelength'] + b
        #     deg = self.pol_degrees[isp]
        #     jacobian_spec_rec = scipy.sparse.coo_matrix(np.vander(rwl, deg+1))
        #     i.append(jacobian_spec_rec.row + slc.start)
        #     j.append(jacobian_spec_rec.col + self.offset[isp])
        #     v.append(jacobian_spec_rec.data)

        # i = np.hstack(i)
        # j = np.hstack(j)
        # v = np.hstack(v)
        # self.jacobian = scipy.sparse.coo_matrix((v, (i, j)), shape=(self.N, self.n)).tocsr()

    def __call__(self, jac=False):
        """Evaluate the recalibration polynomials

            Parameters
            ----------
            jac : bool
                If the jacobian is needed.

            Returns
            -------
            v : numpy.array
                Recalibration parameter evaluated.
            self.jacobian : None or scipy.sparse.coo_matrix
                Jacobian matrix of the recalibration polynomial functions.
            """
        p_full = self.model.pars['SpectrumRecalibration'].full
        v = self.jacobian.dot(p_full)
        if not jac:
            return v, None
        return v, self.jacobian


class SALT2Like(object):
    r"""A re-implementation of the SALT2 model

        SALT2 is an empirical SN spectrophotometric model. This class
        provides a pure python re-implementation of SALT2 with a number of
        improvements.

        The SALT2 parametrization is defined as follows. In the SN restframe
        the absolute spectral density :math:`S(\lambda)` is:

        .. math::

           S(\lambda, \mathrm{p}) = X_0 \times \left[M_0(\lambda, \mathrm{p}) + X_1
           \times M_1(\lambda, \mathrm{p})\right]\ 10^{0.4 c CL(\lambda)}

        where :math:`\mathrm{p}` is the SN phase, i.e. the restframe time since
        SN peak luminosity:

        .. math::

            \mathrm{ph} = \frac{t_{MJD} - t_{max}}{1 + z}

        :math:`M_0`, :math:`M_1` are global surfaces describing the
        spectral evolution of the average SN and its principal variation,
        and :math:`CL(\lambda)` is a global "extinction correction"
        describing the color diversity of the SNIa family.

        :math:`(X_0, X_1, c)` are SN-dependent. :math:`X_0` is the
        amplitude of the "SN-frame B-band lightcurve" as inferred from the
        observer-frame fluxes. :math:`X_1` is the coordinate of the SN
        along :math:`M_1`. In practice, it quantifies the variations of the
        light curve width. :math:`c` is the SN color -- or more exactly,
        the SN color excess with respect to the average SN color.

        Each Light Curve are evaluated interactively to use multi-threading and spectra are evaluated simultaneously.

        Attributes
        ----------
        training_dataset : nacl.dataset.TrainingDataset
            Data set of photometric and spectroscopic observations.
        lc_data : numpy.rec.array
            Photometric data of the training data set.
        phase_range : tuple
            Boundaries for defining the phase interval.
        wl_range : tuple
            Boundaries for defining the wavelength interval.
        n_wl : int
            Number of knot of the wavelength spline basis.
        n_ph : int
            Number of knot of the phase spline basis.
        spectrum_recal_degree : int
            Degree of the spectral recalibration polynomial function.
        init_from_salt2_file : str
            File salt2, created by script 'nacl.simulation.make_salt2_npz.py'.
        delta_phase : float
            Offset in phase wrt SALT2.4.
        dphase_dtmax : numpy.array
            Derivative phase basis wrt time.
        filterpath : str
            Path to the filters files repository in nacl.dev/data/
        timing : list
            Timing of photometric and spectroscopic evaluation.
        basis : nacl.lib.bspline.BSpline2D
            2D spline basis.
        gram : scipy.sparse.csc_matrix
            First order grammian use to evaluate integral product of Wavelength basis of the model and filter basis.
            :math::` \int \lambda B_\ell(\lambda) B_q(\lambda) d\lambda`
        G2 : scipy.sparse.csc_matrix
            Second order grammian use to evaluate integral product of Wavelength basis of the model and filter basis.
            :math::` \int \lambda^2 B_\ell(\lambda) B_q(\lambda) d\lambda`
        L_eff : scipy.sparse.coo_matrix
            Effective wavelength used to calculate the photometric data color law.
        val : numpy.array
            Gather evaluation of each light curve and all spectral data.
        jacobian_val : numpy.array
            Gather non-zero derivatives of each light curve and all spectral data.
        jacobian_i : numpy.array
            Gather data index of non-zero derivatives of each light curve and all spectral data.
        jacobian_j : numpy.array
            Gather parameter index of non-zero derivatives of each light curve and all spectral data.
        filter_basis : nacl.lib.bspline.BSpline
            Filter basis defined common to all the bands.
        color_law : ColorLaw
            Color law class.
        polynome_color_law : array-like
            Photometric color law evaluations.
        jacobian_color_law : scipy.sparse.csr_matrix or None
            Photometric color law matrix of derivatives.
        filter_db : nacl.instruments.FilterDb
            Filter transmission projected on B-splines
        bands : numpy.array
            Bands used for photometric data
        lambda_c : numpy.array
            Mean wavelength of the filter in the SN-restframe.
        lambda_c_red : numpy.array
            Reduced mean wavelength of the filter in the SN-restframe.
        pars : FitParameters
            Model parameters.
        pars0 : numpy.array
            Model initial parameters.
        NORM : float
            Model normalization.
        queue : list
            List of photometric and spectral EvalUnit class.
        disable_cache : object

        """

    def __init__(self, training_dataset,
                 phase_range=(-20., 50.), wl_range=(2000., 9000.),  # . 11000.),
                 basis_knots=[127, 20],
                 basis_filter_knots=900,
                 spectrum_recal_degree=3,
                 init_from_salt2_file=None,
                 init_from_training_dataset=False,
                 normalization_band_name='SWOPE::B',
                 error_snake=None,
                 calib_variance=0.005**2):
        """Constructor.
              - instantiate the bases (phase, wavelength, filter)
              - compute the Grams
              - compute the lambda_eff matrix
              - instantiate a color law and evaluate it on the lambda_eff's
          - organizes the data into spectral/photometric computing units

        Parameters
        ----------
        training_dataset : nacl.dataset.TrainingDataset
            Training dataset.
        phase_range : 2-tuple
            Nominal phase range of the model.
        wl_range : 2-tuple
            Nominal wavelength range of the model.
        basis_knots : 2-list
            Number of wavelength and photometric knot.
        basis_filter_knots : int
            Number of knot for the filter basis
        spectrum_recal_degree : int
            Degree of the spectrum recalibration polynomials
        init_from_salt2_file : str
            If the model is to be initialized with the original
            SALT2-4 surfaces and bases, get them from this file.
        normalization_band_name : str
            Use this band to normalize the model.
        """
        self.training_dataset = training_dataset
        self.lc_data = training_dataset.lc_data
        self.phase_range = phase_range
        self.wl_range = wl_range
        self.n_wl, self.n_ph = basis_knots[0],  basis_knots[1]
        self.basis_knots = basis_knots
        self.basis_filter_knots = basis_filter_knots
        self.spectrum_recal_degree = spectrum_recal_degree
        self.delta_phase = 0. # check: do not remember what this is
        self.filterpath = self.training_dataset.filterpath
        if self.training_dataset.lc_data is not None:
            self.bands = list(self.training_dataset.transmissions.keys())
        self.normalization_band_name = normalization_band_name
        self.calib_variance = calib_variance

        self.timing = []

        self.basis, self.gram, self.G2, self.L_eff = None, None, None, None
        self.val, self.jacobian_val, self.jacobian_i, self.jacobian_j = None, None, None, None
        self.polynome_color_law, self.jacobian_color_law = None, None

        # Filter database
        # TODO: we should be able to optimize this a little
        # (i.e. adapt the filter bases, to lower the size of the grams)
        self.filter_basis = bspline.BSpline(np.linspace(self.wl_range[0], self.wl_range[1],  # 2000., 9000.,  #
                                                        basis_filter_knots), order=4)  # was 9000
        self.filter_db = FilterDb(self.filter_basis, self.training_dataset,
                                  additional_band=[normalization_band_name],
                                  filterpath=self.filterpath)
        self.color_law = ColorLaw()

        n_lc_meas, n_spec_meas, n_spectrophot_meas = \
            self.training_dataset.nb_meas(split_by_type=1)

        # lc = self.training_dataset.lc_data
        # d = dict({(lc[i]['band_id'], lc[i]['Filter']) for i in np.arange(len(lc))})
        # self.bands = np.array([d[i] for i in range(len(d))])
        # self.bands = self.lc_data.band_index

        # lambda_c needed for the color scatter estimation
        # lambda_c = self.training_dataset.lc_data['Wavelength']/(1+self.training_dataset.lc_data['ZHelio'])
        # idx_lam_c = np.array([lc.data['i'][0] for lc in self.training_dataset.lcs])
        # self.lambda_c = lambda_c[idx_lam_c]
        # self.lambda_c_red = self.color_law.reduce(self.lambda_c)
        #
        # TODO: where is this used ?
        # TODO: we may replace this by n_lc_meas > 0
        if self.training_dataset.lc_data is not None:
            tds = self.training_dataset
            ii = self.training_dataset.i_lc_first
            self.lambda_c = tds.lc_data.wavelength[ii] / (1+tds.lc_data.z[ii])
            self.lambda_c_red = self.color_law.reduce(self.lambda_c)

        # initialize degree of the spectral recalibration polynomial
        self._init_spectral_polynomial()

        # initialize model basis and model parameter vector
        # model component: bases, color law, and parameter vector
        self._init_bases()

        # OK. For now, the color scatter and the calibration scatter
        # are explicitely instantiated in the model constructor
        self.calib_scatter = None
        self.color_scatter = None
        self.error_snake = error_snake if error_snake is not None else None
        if self.training_dataset.lc_data is not None:
            self.calib_scatter = vm.CalibrationScatter(self, calib_variance=calib_variance)
            self.color_scatter = vm.ColorScatter(self)
            if self.error_snake is None:
                self.error_snake = vm.SimpleErrorSnake(self)

        # finally, it is better to have it here.
        # NOTE: if there are spectra, the model must be evaluated for them.
        # even if they are marked as invalid
        self.recal_func = None
        if self.training_dataset.spec_data is not None:
            self.recal_func = \
                SpectrumRecalibrationPolynomials(self.training_dataset, self,
                                                 self.recalibration_degree)

        # initialize the global model parameters (M0, M1, CL)
        if init_from_salt2_file:
            self.init_from_salt2(init_from_salt2_file)
        else:
            self.pars = self.init_pars()
        # why ?
        self.pars0 = self.pars.full.copy()

        # initialize the SN specific parameters (X0, X1, col, tmax)
        if init_from_training_dataset:
            self.init_from_training_dataset()

        # we use a default model normalization
        # this is what guarantees that the SALT2.4 absolute mag
        # is -19.5 in the SWOPE::B band. Of course, this default
        # normalization may be changed explicitely, by calling
        # self.renorm(band_name=, Mb=, magsys='AB')
        self.norm = self.normalization(band_name=normalization_band_name,
                                       default_norm=1.01907246e-12)

        # grams
        self.init_grams_and_cc_grid()

        # and finally, prepare the computing units
        self.queue = self._init_computing_units()

        # clear the cache
        self.clear_cache()

        # if we need to run queue units separately,
        # could be useful to disable caching of the results
        self.disable_cache = False

    def clone(self, training_dataset):
        """return a clone (same basis, same color law) for a different tds
        """
        ret = SALT2Like(training_dataset,
                        phase_range=self.phase_range,
                        wl_range=self.wl_range,
                        basis_knots=self.basis_knots,
                        basis_filter_knots=self.basis_filter_knots,
                        spectrum_recal_degree=self.spectrum_recal_degree,
                        normalization_band_name=self.normalization_band_name,
                        calib_variance=self.calib_variance)
        for block_name in ['M0', 'M1', 'CL']:
            ret.pars[block_name].full[:] = self.pars[block_name].full[:]
        ret.norm = ret.normalization(band_name=ret.normalization_band_name)

        return ret

    def init_from_salt2(self, salt2_filename, stick_to_original_model=False):
        """Load & adapt the SALT2.4 global surfaces and color law.

        Load the coefficients of the SALT2.4 surfaces and color law. The
        definition of the model spline bases differs from the original
        definition of the SALT2.4 bases; so, we reproject the original SALT2
        surfaces on the model basis.

        Parameters
        ----------
        salt2_filename : str
            the classical salt2.npz filename containing the definition of the
            SALT2.4 bases, M0, M1 surfaces and color_law.
        """
        f = np.load(salt2_filename)
        phase_grid = f['phase_grid']
        wl_grid = f['wl_grid']
        basis = bspline.BSpline2D(wl_grid, phase_grid, x_order=4, y_order=4)

        if stick_to_original_model:
            # don't remember why we have this
            self.delta_phase = +0.7
            self.basis = basis
            self.pars = self.init_pars()
            self.pars['M0'].full[:] = f['M0'].T.ravel()
            self.pars['M1'].full[:] = f['M1'].T.ravel()
            self.pars['CL'].full[:] = f['CL_pars'][0:4]
            return

        # TODO: replace this with
        # xx = self.basis.bx.grid
        # yy = self.basis.by.grid
        xx = np.linspace(wl_grid[0], wl_grid[-1], basis.bx.nj)
        yy = np.linspace(phase_grid[0], phase_grid[-1], basis.by.nj)
        x,y = np.meshgrid(xx,yy)
        x,y = x.ravel(), y.ravel()
        jac = self.basis.eval(x,y).tocsr()
        factor = cholesky_AAt(jac.T, beta=1.E-20)

        # and initialize the parameters
        self.pars = self.init_pars()
        self.pars['M0'].full[:] = factor(jac.T * f['M0'])
        self.pars['M1'].full[:] = factor(jac.T * f['M1'])
        self.pars['CL'].full[:] = f['CL_pars'][0:4]

    def reduce(self, wl):
        return self.color_law.reduce(wl)

    def init_grams_and_cc_grid(self):
        r"""Compute the :math:`\Lambda^{\mathrm{eff}}_{\ell q}` matrix (see definition above) on which the color
        law is evaluated.

        .. math::
             \bar{\lambda}_{\ell q} = \frac{\int \lambda^2 B_\ell(\lambda) B_q(\lambda)
             d\lambda}{\int \lambda B_\ell(\lambda) B_q(\lambda) d\lambda}

        Compute de grammian of order one, :math:`G` and two :math:`G2` of the model :

        .. math::
            G = \int \lambda B_\ell(\lambda) B_q(\lambda) d\lambda \\
            G2 = \int \lambda^2 B_\ell(\lambda) B_q(\lambda) d\lambda


        .. note::
             this method will be moved to the main model class (since we may work
             with one single :math:`\Lambda^{\mathrm{eff}}` matrix in a near future).
        """
        self.gram = get_gram(0., self.basis.bx, self.filter_basis, lambda_power=1)
        self.G2 = get_gram(0., self.basis.bx, self.filter_basis, lambda_power=2)

        gram = self.gram.tocoo()
        gram2 = self.G2.tocoo()
        assert(~np.any(gram.row-gram2.row) and ~np.any(gram.col-gram2.col))
        l_eff = gram2.data / gram.data
        self.L_eff = scipy.sparse.coo_matrix((l_eff, (gram.row, gram.col)), shape=gram.shape)

    def get_struct(self):
        """return the structure of the fit parameter vector

        In practice, the fit parameter vector is larger than just the model
        parameters: it also contains the parameters of the error models (error
        snake, color scatter, calibration, see e.g. variancemodels.py). The
        instantiation of the final fit parameter vector cannot therefore be
        performed by the model itself.  What the model can do, is to return the
        description of the fit parameter blocks it knows about.
        """
        nb_sne = self.training_dataset.nb_sne()
        # nb_spectra = self.training_dataset.nb_spectra()
        # nb_passbands = len(self.bands)
        spec_recalibration_npars = self.recalibration_degree + 1
        nb_lightcurves = self.training_dataset.nb_lcs(valid_only=False)
        d = [('X0',   nb_sne),
             ('X1',   nb_sne),
             ('col',  nb_sne),
             ('tmax', nb_sne),
             ('M0',   self.basis.bx.nj * self.basis.by.nj),
             ('M1',   self.basis.bx.nj * self.basis.by.nj),
             ('CL',  4)]
        if self.training_dataset.spec_data is not None:
            d.append(('SpectrumRecalibration', spec_recalibration_npars.sum()))

             #             ('eta_calib', nb_passbands),
             #             ('kappa_color', nb_lightcurves)
             # ]
        return d

    def init_pars(self):
        """instantiate a fit parameter vector

        Returns
        -------
        fp : nacl.lib.fitparameters.FitParameters
            Model parameters.
        """
        p_struct = self.get_struct()
        if self.calib_scatter is not None:
            p_struct.extend(self.calib_scatter.get_struct())
        if self.color_scatter is not None:
            p_struct.extend(self.color_scatter.get_struct())
        if self.error_snake is not None:
            p_struct.extend(self.error_snake.get_struct())
        fp = FitParameters(list(set(p_struct)))

        # minimal initialization
        fp['X0'].full[:] = 1.
        if 'SpectrumRecalibration' in fp._struct:
            assert self.recal_func is not None
            fp['SpectrumRecalibration'].full[:] = self.recal_func.init_pars()
        return fp

    def init_from_training_dataset(self):
        """load initial sn parameters from the training dataset
        """
        sn_data = self.training_dataset.sn_data
        self.pars['X0'].full[sn_data.sn_index] = sn_data.x0
        self.pars['X1'].full[sn_data.sn_index] = sn_data.x1
        self.pars['col'].full[sn_data.sn_index] = sn_data.col
        self.pars['tmax'].full[sn_data.sn_index] = sn_data.tmax

#        nb_sne = self.training_dataset.nb_sne()
#        nb_spectra = self.training_dataset.nb_spectra()
#        nb_passbands = len(self.bands)
#        all_degree = self.recalibration_degree + 1
#        nb_lightcurves = self.training_dataset.nb_lcs()
#        fp = FitParameters([('X0', nb_sne),
#                            ('X1', nb_sne),
#                            ('col',  nb_sne),
#                            ('tmax', nb_sne),
#                            ('M0',  self.basis.bx.nj * self.basis.by.nj),
#                            ('M1',  self.basis.bx.nj * self.basis.by.nj),
#                            ('CL',  4),
#                            # TODO: size of recalibration parameters should be abstracted
#                            ('SpectrumRecalibration', all_degree.sum()),
#                            ('eta_calib', nb_passbands),
#                            ('kappa_color', nb_lightcurves)])

#        fp['X0'].full[:] = 1.
#        rec_val = np.zeros_like(fp['SpectrumRecalibration'].full[:])

#        for i in np.arange(nb_spectra):
#            offset = all_degree[:i+1].sum()
#            rec_val[offset-1] = 1  # -0.2

#        fp['SpectrumRecalibration'].full[:] = rec_val  # + 0.2
#        fp['kappa_color'].full[:] = 0  # 1e-1
#        return fp

    def _init_spectral_polynomial(self):
        """instantiate the recalibration polynomials

        if a degree is specified, all spectra have the same degree.
        Since the degree of the polynomial must not exceed the number of Light curves :
        this degree is large odd number inferior to the numbers of light curves for this SN.
        """
        # note: the model is evaluated on the full dataset.
        # not just the valid data.
        nb_spectra = self.training_dataset.nb_spectra(valid_only=False)
        self.recalibration_degree = np.full(nb_spectra, self.spectrum_recal_degree)

        # here, there was a code to limit the degree of the recalibration
        # polynomials to the total number of light curves available for the
        # corresponding SN.

        # if self.spectrum_recal_degree is None:
        #     # print(self.spectrum_recal_degree)
        #     lcs = self.training_dataset.lc_data
        #     sps = self.training_dataset.spec_data

        #     for isp in sps.spec_set:
        #         isn =
        #     for isp in np.unique(sps['spec_id']):
        #         isn = sps['sn_id'][sps['spec_id'] == isp][0]
        #         n_lcs_sn = len(np.unique(lcs[lcs['sn_id'] == isn]['lc_id']))
        #         if n_lcs_sn % 2 == 0:
        #             self.recalibration_degree[isp] = n_lcs_sn - 1
        #         elif n_lcs_sn % 2 == 1:
        #             self.recalibration_degree[isp] = n_lcs_sn - 2
        # else:
        #     self.recalibration_degree *= self.spectrum_recal_degree

    def _init_bases(self):
        """
        Instantiate model bases
        """
        phase_grid = np.hstack([np.linspace(self.phase_range[0], self.phase_range[1], self.n_ph)])
        wl_grid = np.linspace(self.wl_range[0], self.wl_range[1], self.n_wl)
        self.basis = bspline.BSpline2D(wl_grid, phase_grid, x_order=4, y_order=4)

    def normalization(self, band_name='SWOPE::B', Mb=-19.5, magsys='AB',
                      default_norm=None):
        """model normalization

        The SALT2Like normalization is set during training by the constraint
        on the integral of M0 at phase zero.

        Therefore, by default, we do not renormalize the model during
        evaluation.
        """
        tq, filter_basis = self.filter_db[band_name]
        phase_eval = self.basis.by.eval(np.array([0. + self.delta_phase])).tocsr()
        gram = get_gram(z=0., model_basis=self.basis.bx,
                        filter_basis=filter_basis, lambda_power=1)
        surface_0 = self.pars['M0'].full.reshape(len(self.basis.by), -1)
        # evaluate the integral of the model in the specified band
        self.int_M0_phase_0 = phase_eval.dot(surface_0.dot(gram.dot(tq)))

        # AB flux in the specified band
        ms = MagSys(magsys)
        zp = ms.ZeroPoint(self.filter_db.transmission_db[band_name])
        self.int_ab_spec = 10**(0.4 * zp)

        # normalization quantities
        self.flux_at_10pc = np.power(10., -0.4 * (Mb-zp))
        self.flux_at_10Mpc = np.power(10., -0.4 * (Mb+30.-zp))

        if default_norm is not None:
            return default_norm

        return self.flux_at_10Mpc / self.int_M0_phase_0

    def renorm(self, band_name='SWOPE::B', Mb=-19.5, magsys='AB'):
        """Adjust the model normalization
        """
        # explicitely recompute a normalization
        self.norm = self.normalization(band_name, Mb, magsys,
                                       default_norm=None)

    def _init_computing_units(self):
        """Prepare and queue all the computing units

        The model evaluation is deferred to two kinds of so-called
        'eval units'.

            - Photometric eval units, which compute the light curves
              (i.e. the integral of the SALT2 surfaces). In our current
              design, a Photometric eval unit predicts the lightcurve
              for a given SN in a given band.
            - Spectroscopic eval units, which predict SN spectra.
              In our current design, a spectroscopic eval unit
              predicts one spectrum for a given SN.

        All units are grouped in a single execution queue.

        .. note:: we designed things like this because we had some
             hope that we could gain in speed from using explicit
             parallelism (using joblib or some similar framework).  In
             practice, it seems that the overheads from using python
             parallelism at this level are high (because of the GIL)
             and that we gain much more by using numpy/scipy implicit
             multithreading. We stick to this design because it makes
             things clearer in fact.

        """
        # n_lc_meas, n_spec_meas, n_spectrophot_meas = \
        #     self.training_dataset.nb_meas(valid=True, split_by_type=True)
        queue = []
        if self.training_dataset.lc_data is not None:
            for lc in self.training_dataset.lcs:
                queue.append(LightcurveEvalUnitTz(lc, self))
        if self.training_dataset.spec_data is not None:
            queue.append(SpectrumEvalUnitFast(self.training_dataset, self))
        if self.training_dataset.spectrophotometric_data is not None:
            queue.append(SpectroPhotoEvalUnit(self.training_dataset, self))
        return queue

    def update_computing_units(self, ilc=None, spec=False):
        """
        Recreate the model queue as a function of the wanted LCs and spectra.

        Parameters
        -------
        ilc : None or int
            If None all light curve are evaluated, else only teh desired one.
        spec : bool
            Whether Spectra need to be evaluated.

        Returns
        -------
        queue : list
            The new queue
        """
        queue = []
        if ilc is not None:
            for lc in [self.training_dataset.lcs[ilc]]:
                queue.append(LightcurveEvalUnitTz(lc, self))
        if spec:
            queue.append(SpectrumEvalUnitFast(self.training_dataset, self))
        return queue

    def clear_cache(self):
        """
        Clear model evaluation, derivatives and timing.
        """
        self.val = []
        self.jacobian_i = []
        self.jacobian_j = []
        self.jacobian_val = []
        self.timing = []

    def precompute_color_law(self, cl_pars=None, jac=False):
        """
        Precompute the color law for the photometric data.

        Parameters
        -------
        cl_pars : None or numpy.array
            Color law parameters
        jac : bool
            If derivatives are needed.
        """
        if cl_pars is None:
            cl_pars = self.pars['CL'].full

        polynome_color_law, jacobian_color_law = \
            self.color_law(self.L_eff.data, cl_pars,
                           jac=jac)  # return_jacobian_as_coo_matrix=False)
        self.polynome_color_law = \
            scipy.sparse.csr_matrix((polynome_color_law,
                                     (self.L_eff.row, self.L_eff.col)),
                                    shape=self.L_eff.shape)
        if jac:
            self.jacobian_color_law = []
            _, n = jacobian_color_law.shape
            for i in range(n):
                jacobian_cl = \
                    scipy.sparse.csr_matrix((jacobian_color_law[:, i],
                                             (self.L_eff.row, self.L_eff.col)), shape=self.L_eff.shape)
                self.jacobian_color_law.append(jacobian_cl)

    def get_restframe_phases(self, data):
        """
        Given a chunk of data, return the restframe phases

        Returns
        -------
        numpy.array
            data SN-restframe phase
        """
        sn_index = data.sn_index
        tmax = self.pars['tmax'].full[sn_index]
        return (data.mjd - tmax) / (1.+data.z)

    def __call__(self, p, jac=False, plotting=False, ilc_plot=None, spec_plot=False):
        """Evaluate the model for the parameter set p

        In practice, loop over the queue and run each eval unit.
        Assemble the results into one single vector and (optionally)
        one single jacobian matrix.

        Parameters
        -------
        p : numpy.array
            Vector containing the free parameters only.
        jac : bool
            Whether it return the jacobian matrix.

        plotting : bool
            Plotting need to evaluated only some data [plotting needs]
        ilc_plot : list
            Light curves to be evaluated [plotting needs]
        spec_plot : bool
            Spectra to be evaluated [plotting needs]

        Returns
        -------
        val : numpy.array
            model results
        jacobian : scipy.sparse.csr_matrix
            jacobian matrix (if jac is true)
        """
        # update pars
        self.pars.free = p

        # pre-evaluate the color law (shared between all light curves)
        self.precompute_color_law(jac=jac)

        # precompute the values of the phase basis on the full dataset
        # significantly faster that way
        if self.training_dataset.lc_data is not None:
            restframe_phases = self.get_restframe_phases(self.lc_data)
            self.phase_eval = self.basis.by.eval(restframe_phases + self.delta_phase).tocsr()
            if jac:
                self.dphase_dtmax = self.basis.by.deriv(restframe_phases + self.delta_phase).tocsr()
            else:
                self.dphase_dtmax = None

        self.clear_cache()

        # queue all Eval Unit for minimization or for plotting
        if plotting:
            queue = self.update_computing_units(ilc=ilc_plot, spec=spec_plot)
        else:
            queue = self.queue

        # now, we are ready to loop over the eval units
        for q in queue:
            q(jac)
        val = np.hstack(self.val)
        # print('--> len(val):', len(val), len(self.training_dataset.lc_data), len(self.training_dataset.spec_data))

        if not jac:
            return val

        # collect and assemble the results
        # n_data = len(self.training_dataset.lc_data)  + len(self.training_dataset.spec_data)
        n_data = self.training_dataset.nb_meas(valid_only=False)

        # nrl: I don't know what this is for. Commented out.
        # fit_spec = False
        # for ique in self.queue:
        #     if ique.data['spec_id'].mean() != -1:
        #         fit_spec = True

        # if fit_spec:
        #     n_data += len(self.training_dataset.spec_data)

        logging.debug('computing derivatives: hstack...')
        n = len(self.pars.free)
        i = np.hstack(self.jacobian_i)
        j = np.hstack(self.jacobian_j)
        v = np.hstack(self.jacobian_val)
        logging.debug('building coo_matrix...')
        idx = j >= 0  # self.pars.indexof(j) >= 0
        jacobian = scipy.sparse.coo_matrix((v[idx], (i[idx], j[idx])), shape=(n_data, n))
        logging.debug('ok, done.')
        return val, jacobian

#       else:
#            logging.info('SALT2Like.__call__: joblib.Parallel')
#            def f(x):
#                x.__call__(jac=jac)
#            Parallel(n_jobs=n_jobs)(delayed(f)(x) for x in self.queue)
#        self.assemble(res)

# move this into model (cache needs to be associated with the bases)


_G, _G2 = {}, {}


def get_gram(z, model_basis, filter_basis, lambda_power=1):
    """
    Calculate the grammian of to spline basis.

    The grammian :math:`G` of order :math:`N`, to basis :math:`B_0` (define on wavelength,
    in our case surfaces wavelength basis) and
    :math:`B_1` (define on SN-restframe wavelength, filter basis) is defined as :

    .. math::
        G = \\int \\lambda^N B_0(\\lambda) B_q(\\lambda (1+z)) d\\lambda

    Parameters
    -------
    z : numpy.array
        Vector containing the data redshift.
    model_basis : nacl.lib.bspline.BSpline
        Wavelength basis.
    filter_basis : nacl.lib.bspline.BSpline
        Filter basis defined common to all the bands.
    lambda_power : int
        Grammian order.

    Returns
    -------
    gram : scipy.sparse.csc_matrix
        Grammian
    """
    global _G
    global _G2
    key = (z, model_basis, filter_basis, lambda_power)

    gram = _G.get(key, None)
    if gram is None:
        gram = bspline.lgram(model_basis, filter_basis, z=z, lambda_power=lambda_power).tocsc()
        _G[key] = gram

    return gram


class LightcurveEvalUnitTz(object):
    r"""
    Compute an SN light curve of one supernova in one single band.

    This class is one of the two types of "computing unit". Given a
    set of dates, and the :math:`(X_0, X_1, c, t_{max})` parameters of
    the SN, compute the quantities:

    .. math::

         X_0 \times (1+z) \times \left[I_0 + X_1 I_1\right]

    with

    .. math::
         I_{0|1} = \int M_{0|1}(\lambda, \mathrm{p}) \frac{\lambda}{hc} T((1+z)\lambda) 10^{0.4\ c\ P(\lambda)} d\lambda

    In practice, we can speed up the computations by decomposing the
    filter on a spline basis: :math:`T(\lambda (1+z)) = \sum_q t_q(z)
    B_q(\lambda)= \sum_q (1+z) t_q B_q(\lambda)`, which allows to decompose the integral above as:

    .. math::
        I_{0|1} = \sum_{k\ell q} \theta_{0|1, k\ell} t_q(z) B_k(\mathrm{p})\ \int B_\ell(\lambda)
        \frac{\lambda}{hc} B_q(\lambda)\ 10^{0.4\ c\ P(\lambda)} d\lambda

    We use the fact that the color law is a slowly variable function
    of :math:`\lambda` (compared to the individual splines) to expel the
    color law from the integral:

    .. math::
       \int B_\ell(\lambda) \frac{\lambda}{hc} B_q(\lambda) CL(\lambda) d\lambda \approx
       CL(\lambda^{\mathrm{eff}}_{\ell q})\ \times \int B_\ell(\lambda) \frac{\lambda}{hc} B_q(\lambda) d\lambda

    up to second order, if we define:

    .. math::
       \lambda^{\mathrm{eff}}_{\ell q} = \frac{\int B_\ell(\lambda)
       \lambda^2 B_q(\lambda) d\lambda}{\int B_\ell(\lambda) \lambda B_q(\lambda) d\lambda}


    and so, defining: :math:`\Lambda^{\mathrm{eff}} = (\lambda^{\mathrm{eff}}_{\ell q})` and
    ::math:`G = (G_{\ell q}) = (\int B_\ell(\lambda)\frac{\lambda}{hc} B_q(\lambda)) d\lambda`,
    the integral evaluation reduces to:

    .. math::
        I_{0|1} = J\ \cdot \Theta\ \cdot \left[G \Lambda^{\mathrm{eff}}\right] \cdot t_z

    where :math:`J`, :math:`G`,
    :math:`\Lambda^{\mathrm{eff}}` and :math:`t_z` are sparse
    and where :math:`G, \Lambda^{\mathrm{eff}}`
    can be precomputed once for all.

    Matrix :math:`G` is called the Gramian of the model and
    filter spline bases. It is precomputed exactly, using Gaussian
    quadrature when the model is instantiated.

    This strategy decompose :math:`T((1+z)\lambda)` and work with a single Gramian and
    an SN-dependant :math:`t_z` vector.
    This option is probably computationally less intensive, as we can
    factorize the evaluation of the color law.

    Attributes
    ----------
    lcdata : nacl.dataset.LcData
        Photometric of one Lc of one SN nacl data class.
    data : numpy.rec.array
        Photometric data in nacl data file type.
    model : nacl.models.salt.SALT2Like
        Model.
    z : numpy.array
        SN redshift of Lc observation.
    band : numpy.array
         SN band of Lc observation.
    tqz : numpy.array
         :math:`t_z`.
    sn_id : numpy.array
        SNe index of all data.
    ph_basis_size ; int
        Number of phase basis knots.
    M0 : numpy.array
        M_0 parameters reshape as 2D array, (wavelength, phase) matrix.
    M1 : numpy.array
        M_1 parameters reshape as 2D array, (wavelength, phase) matrix.
    cl_pars : numpy.array
        Color law parameters.
    """

    def __init__(self, lcdata, model):
        r"""Constructor
        Retrieve the band shape :math:`T(\lambda)` and project :math:`T(\lambda(1+z))` on the basis

        Parameters
        ----------
        lcdata : nacl.dataset.LcData
            Photometric of one Lc of one SN nacl data class.
        model : nacl.models.salt.SALT2Like
            Model.
        """
        self.lcdata = lcdata
        # self.data = lcdata.data # we no longer use this
        self.model = model
        self.z = lcdata.z[0]
        self.band = lcdata.band[0]
        tr = model.filter_db.transmission_db[self.band]
        self.tqz, _ = model.filter_db.insert(tr, z=self.z)
        # set to zero very small values
        self.tqz[(np.abs(self.tqz)/self.tqz.max() < 1e-10)] = 0.

        # self.sn_id = lcdata.sn_id
        self.sn_index = lcdata.sn_index[0]

        #        self.wl_basis_size = len(model.basis.bx)
        self.ph_basis_size = len(model.basis.by)

        self.M0 = model.pars['M0'].full.reshape(self.ph_basis_size, -1)
        self.M1 = model.pars['M1'].full.reshape(self.ph_basis_size, -1)
        self.cl_pars = model.pars['CL'].full

    def __call__(self, jac=False, debug_mode=False):
        """
        Evaluate the SN light curve.

        Parameters
        ----------
        jac : bool
            Whether it return the jacobian matrix
        debug_mode : bool
            if True, return the model components instead of the
            model results.

        Returns
        ----------
        val : numpy.array
            Model evaluation
        jacobian : scipy.sparse.csr_matrix
            Jacobian matrix (optional)

        """
        t0 = time.perf_counter()
        sn_index = self.sn_index
        zz = 1. + self.z
        pars = self.model.pars
        # data = self.lcdata.data
        band_index = self.lcdata.band_index[0]

        # band_id = self.lcdata.data['band_id'][0]
        # print(self.model.bands[band_id], self.lcdata.data['Filter'][0])
        # lc_id = self.lcdata.data['lc_id'][0]
        lc_index = self.lcdata.lc_index[0]
        sn_index = self.lcdata.sn_index[0]

        # sn-related parameters
        x0, x1 = pars['X0'].full[sn_index], pars['X1'].full[sn_index]
        c, tmax = pars['col'].full[sn_index],  pars['tmax'].full[sn_index]
        eta = pars['eta_calib'].full[band_index]
        kappa = pars['kappa_color'].full[lc_index]
        # model_to_meas_scale = self.lc_data.norm
        flux_scale = self.model.norm * self.lcdata.norm

        phase_eval = self.model.phase_eval[self.lcdata.slc]
        # color law evaluation -- on the Gram \lambda_eff's
        cl = np.power(10., 0.4 * c * self.model.polynome_color_law.data)
        csr_color_law = scipy.sparse.csr_matrix((cl, (self.model.L_eff.row, self.model.L_eff.col)),
                                                shape=self.model.L_eff.shape)
        gram = self.model.gram.multiply(csr_color_law)
        tqz = self.tqz

        # much faster with the .dot's (instead of @)
        integral_surface_0 = phase_eval.dot(self.M0.dot(gram.dot(tqz)))
        integral_surface_1 = phase_eval.dot(self.M1.dot(gram.dot(tqz)))
        flux = flux_scale * zz * x0 * (integral_surface_0+x1*integral_surface_1)*(1+eta)*(1+kappa)

        # if debug_mode:
        #     return model_norm * integral_surface_0, model_norm * integral_surface_1, \
        #            cl, flux, x0, x1, model_norm

        self.model.val.append(flux)
        if not jac:
            self.model.timing.append(time.perf_counter()-t0)
            return flux

        # n_data = len(self.lcdata)
        # sn_index = np.full(n_data, self.sn_index)
        # norm = self.model.norm

        # shortcut names to the internal cache holding the
        # jacobian matrix definition
        jacobian_i, jacobian_j, jacobian_val = self.model.jacobian_i, self.model.jacobian_j, self.model.jacobian_val

        # dMdX0
        jacobian_i.append(self.lcdata.row)
        jacobian_j.append(self.model.pars['X0'].indexof(self.lcdata.sn_index))
        assert len(self.lcdata.row) == len(self.model.pars['X0'].indexof(self.lcdata.sn_index))
        jacobian_val.append(flux_scale * zz * (integral_surface_0 + x1*integral_surface_1) * (1+eta) * (1+kappa))

        # dMdX1
        jacobian_i.append(self.lcdata.row)
        jacobian_j.append(self.model.pars['X1'].indexof(self.lcdata.sn_index))
        assert len(self.lcdata.row) == len(self.model.pars['X1'].indexof(self.lcdata.sn_index))
        jacobian_val.append(flux_scale * zz * x0 * integral_surface_1 * (1+eta) * (1+kappa))

        # dMdc
        jacobian_i.append(self.lcdata.row)
        jacobian_j.append(self.model.pars['col'].indexof(self.lcdata.sn_index))
        assert len(self.lcdata.row) == len(self.model.pars['col'].indexof(self.lcdata.sn_index))
        gram_color_law = gram.multiply(self.model.polynome_color_law)
        dintegral0_dc = 0.4 * np.log(10.) * phase_eval.dot(self.M0.dot(gram_color_law.dot(tqz)))
        dintegral1_dc = 0.4 * np.log(10.) * phase_eval.dot(self.M1.dot(gram_color_law.dot(tqz)))
        jacobian_val.append(flux_scale * zz * x0 * (dintegral0_dc + x1*dintegral1_dc) * (1+eta) * (1+kappa))

        # dMdtmax
        dphase_dtmax = self.model.dphase_dtmax[self.lcdata.slc]
        jacobian_i.append(self.lcdata.row)
        jacobian_j.append(self.model.pars['tmax'].indexof(self.lcdata.sn_index))
        assert len(self.lcdata.row) == len(self.model.pars['tmax'].indexof(self.lcdata.sn_index))
        dintegral0_dtmax = -dphase_dtmax.dot(self.M0.dot(gram.dot(tqz))) / zz
        dintegral1_dtmax = -dphase_dtmax.dot(self.M1.dot(gram.dot(tqz))) / zz
        jacobian_val.append(flux_scale * zz * x0 * (dintegral0_dtmax + x1*dintegral1_dtmax)*(1+eta)*(1+kappa))

        # dMdtheta_0
        dbase_dtheta = scipy.sparse.kron(phase_eval, gram.dot(tqz)).tocoo()
        jacobian_i.append(self.lcdata.row[dbase_dtheta.row])
        jacobian_j.append(self.model.pars['M0'].indexof(dbase_dtheta.col))
        assert len(self.lcdata.row[dbase_dtheta.row]) == len(self.model.pars['M0'].indexof(dbase_dtheta.col))
        jacobian_val.append(flux_scale[dbase_dtheta.row] * zz * x0 * dbase_dtheta.data * (1+eta) * (1+kappa))

        # dMdtheta_1
        jacobian_i.append(self.lcdata.row[dbase_dtheta.row])
        jacobian_j.append(self.model.pars['M1'].indexof(dbase_dtheta.col))
        assert len(self.lcdata.row[dbase_dtheta.row]) == len(self.model.pars['M1'].indexof(dbase_dtheta.col))
        jacobian_val.append(flux_scale[dbase_dtheta.row] * zz * x0 * x1 * dbase_dtheta.data * (1+eta) * (1+kappa))

        # dMdcl
        # I really don't know how to vectorize the computation
        # of these derivatives. If somebody has an idea let me know.
        buff = np.zeros(len(self.lcdata)).astype(int)
        for i, jacobian_color_law in enumerate(self.model.jacobian_color_law):
            buff[:] = i
            jacobian_i.append(self.lcdata.row)
            jacobian_j.append(self.model.pars['CL'].indexof(buff))
            gram_jacobian_color_law = gram.multiply(jacobian_color_law)
            jacobian_surface0_color_law = 0.4 * np.log(10.) * c * phase_eval.dot(self.M0.dot(
                gram_jacobian_color_law.dot(tqz)))
            jacobian_surface1_color_law = 0.4 * np.log(10.) * c * phase_eval.dot(self.M1.dot(
                gram_jacobian_color_law.dot(tqz)))
            jacobian_val.append(flux_scale * zz * x0 * (jacobian_surface0_color_law + x1*jacobian_surface1_color_law)
                                * (1+eta) * (1+kappa))

        # dMdeta
        jacobian_i.append(self.lcdata.row)
        jacobian_j.append(self.model.pars['eta_calib'].indexof(self.lcdata.band_index))
        jacobian_val.append(flux_scale * x0 * zz * (integral_surface_0 + x1*integral_surface_1)*(1+kappa))

        # dKappa
        jacobian_i.append(self.lcdata.row)
        jacobian_j.append(self.model.pars['kappa_color'].indexof(self.lcdata.band_index))
        jacobian_val.append(flux_scale * x0 * zz * (integral_surface_0 + x1*integral_surface_1) * (1+eta))

        if self.model.disable_cache:
            self.model.clear_cache()
        self.model.timing.append(time.perf_counter()-t0)
        return flux


class SpectrumEvalUnitFast(object):
    r"""Evaluate the model for all SN spectra in the training dataset

    This class is one of the two type of "eval units". Given a chunk
    of the training dataset which corresponds the spectral observations,
    and given the :math:`(X_0, X_1, c, t_{max})` parameters
    of the SN, compute the quantity:

    .. math::

         \frac{1}{1+z} \left[M_0\left(\frac{\lambda}{1+z}, \mathrm{p}\right) + X_1\ M_1\left(\frac{\lambda}{1+z},
         \mathrm{p}\right) \right]\ 10^{0.4\ c\ P(\frac{\lambda}{1+z})}\ s(\lambda_{rec})

    where

    .. math::
        M_{0|1}(\lambda, \mathrm{p}) = \sum_{k\ell} \theta_{k\ell} B_k(\mathrm{p}) B_l(\mathrm{\lambda})

    and

    .. math::
         \mathrm{p} = \frac{t - t_{max}}{1+z}

    and where :math:`R_s(\lambda)` is a polynomial correction which
    absorbs the wavelength-dependent large scale calibration errors
    affecting the spectrum.

    Again, the evaluation reduces to a sparse matrix multiplication.

    Attributes
    ----------
    training_dataset : nacl.dataset.TrainingDataset
        Data set of photometric and spectroscopic observations.
    data : nacl.dataset.SpectrumData
        Spectra of all SNe in the training dataset.
    model : nacl.models.salt.SALT2Like
        Model.
    z : numpy.array
        SN redshift of Lc observation.
    spec_id : numpy.array
        spectrum index of all data.
    sn_id : numpy.array
        SNe index of all data.
    ph_basis_size : int
        Number of phase basis knots.
    wl_basis_size : int
        Number of wavelength basis knots.
    restframe_wl : numpy.array
        SNe-restframe wavelength for all spectra.
    recal_func : SpectrumRecalibrationPolynomials
        Recalibration polynomial.
    M0 : numpy.array
        M_0 parameters reshape as 2D array, (wavelength, phase) matrix.
    M1 : numpy.array
        M_1 parameters reshape as 2D array, (wavelength, phase) matrix.
    cl_pars : numpy.array
        Color law parameters.

    """
    def __init__(self, tds, model):
        """Constructor.

        Parameters
        ----------
        tds : nacl.dataset.TrainingDataset
            Data set of photometric and spectroscopic observations.
        model : nacl.models.salt.SALT2Like
            Model.
        """
        self.training_dataset = tds
        self.data = tds.spec_data
        self.model = model

        self.spec_index = self.data.spec_index
        self.sn_index = self.data.sn_index
        # self.z = self.training_dataset.sn_data.z[self.sn_id]
        self.z = self.data.z

        # Look at that later
        self.color_law = model.color_law
        self.pars = model.pars
        self.basis = model.basis

        self.wl_basis_size = len(model.basis.bx)
        self.ph_basis_size = len(model.basis.by)

        # restframe wavelengths
        self.restframe_wl = self.data.wavelength/(1.+self.z)
        #        self.Jl = model.basis.bx.eval(self.restframe_wl).tocsr()

        # and we can connect directly to the global parameters
        self.M0 = model.pars['M0'].full
        self.M1 = model.pars['M1'].full
        self.cl_pars = model.pars['CL'].full

        # recalibration polynomial (one per spectrum, because we adapt to the spectrum wavelength range)
        #        self.recal_func = SpectrumRecalibrationPolynomials(self.training_dataset, self.model,
        #                                                           self.model.recalibration_degree)
        self.recal_func = self.model.recal_func

    def __call__(self, jac=False, debug_mode=False):
        r"""
        Evaluate the model for a all spectra

        Parameters
        ----------
        jac : bool
            if True compute and return the jacobian matrix
        debug_mode : bool
            if true, just return the model components.

        Returns
        -------
        val : numpy.array
            Model evaluations.
        jacobian : scipy.sparse.csr_matrix
            Jacobian matrix (if jac is true).
        """
        t0 = time.perf_counter()
        pars = self.pars

        # sn-related parameters
        x0, x1 = pars['X0'].full[self.sn_index], pars['X1'].full[self.sn_index]
        c, tmax = pars['col'].full[self.sn_index],  pars['tmax'].full[self.sn_index]

        # we need to re-evaluate the basis on the phases, since tmax changes
        restframe_phases = (self.data.mjd-tmax)/(1.+self.z)
        jacobian = self.basis.eval(self.restframe_wl, restframe_phases + self.model.delta_phase).tocsr()

        # model components
        component_0 = jacobian.dot(self.M0)
        component_1 = jacobian.dot(self.M1)
        polynome_color_law, jacobian_color_law = self.color_law(self.restframe_wl, self.cl_pars, jac=jac)
        color_law = np.power(10., 0.4*c*polynome_color_law)
        zz = 1. + self.z

        # recalibration polynomial
        # if we evaluate this, then recal_func must be instantiated
        # if self.recal_func is not None:
        assert self.recal_func is not None
        recal, jacobian_spec_rec = self.recal_func(jac=jac)
        if jacobian_spec_rec is not None:
            jacobian_spec_rec = jacobian_spec_rec.tocoo()
            # don't know what to do with this
            # jacobian_spec_rec.data *= recal[jacobian_spec_rec.row]

        # recal = np.exp(recal)
        pca = (component_0 + x1 * component_1)
        model = pca * color_law * recal / zz

        if debug_mode:
            return component_0, component_1, color_law, recal, model

        self.model.val.append(model)
        if not jac:
            self.model.timing.append(time.perf_counter()-t0)
            return model

        jacobian = jacobian.tocoo()
        # X0 does not appear in the spectral part of the model
        # hence, dmdX0 = 0

        # dMdX1
        jacobian_i, jacobian_j, jacobian_val = self.model.jacobian_i, self.model.jacobian_j, self.model.jacobian_val
        jacobian_i.append(self.data.row)
        jacobian_j.append(self.model.pars['X1'].indexof(self.sn_index))
        jacobian_val.append(component_1 * color_law * recal / zz)

        # dMdc
        jacobian_i.append(self.data.row)
        jacobian_j.append(self.model.pars['col'].indexof(self.sn_index))
        jacobian_val.append(model * 0.4 * np.log(10.) * polynome_color_law)

        # dMdtmax
        # we can gain a little here, by not evaluating the gradient along the wavelength (ddlambda)
        _, deval_phase = self.model.basis.gradient(self.restframe_wl, restframe_phases + self.model.delta_phase)
        deval_phase = deval_phase.tocsr()
        jacobian_i.append(self.data.row)
        jacobian_j.append(self.model.pars['tmax'].indexof(self.sn_index))
        jacobian_val.append(-1. * (deval_phase.dot(self.M0) + x1*deval_phase.dot(self.M1)) * color_law * recal / zz**2)

        # dmdtheta_0
        jacobian_i.append(self.data.row[jacobian.row])
        jacobian_j.append(self.model.pars['M0'].indexof(jacobian.col))
        jacobian_val.append(jacobian.data * color_law[jacobian.row] * recal[jacobian.row] / zz[jacobian.row])

        # dmdtheta_1
        jacobian_i.append(self.data.row[jacobian.row])
        jacobian_j.append(self.model.pars['M1'].indexof(jacobian.col))
        jacobian_val.append(x1[jacobian.row] * jacobian.data * color_law[jacobian.row] *
                            recal[jacobian.row] / zz[jacobian.row])

        # dMdcl (color law)
        jacobian_color_law = scipy.sparse.coo_matrix(jacobian_color_law)
        jacobian_i.append(self.data.row[jacobian_color_law.row])
        jacobian_j.append(self.model.pars['CL'].indexof(jacobian_color_law.col))
        jacobian_val.append(c[jacobian_color_law.row] * 0.4 * np.log(10.) * jacobian_color_law.data *
                            model[jacobian_color_law.row])

        # dMdr (recalibration)
        if jacobian_spec_rec is not None:
            jacobian_i.append(self.data.row[jacobian_spec_rec.row])
            jacobian_j.append(self.model.pars['SpectrumRecalibration'].indexof(jacobian_spec_rec.col))
            jacobian_val.append(jacobian_spec_rec.data * (pca*color_law)[jacobian_spec_rec.row]/zz[jacobian_spec_rec.row])

        if self.model.disable_cache:
            self.model.clear_cache()
        self.model.timing.append(time.perf_counter()-t0)

        return model


class SpectroPhotoEvalUnit(object):

    def __init__(self, tds, model):
        """Constructor.

        Parameters
        ----------
        tds : nacl.dataset.TrainingDataset
            Data set of photometric and spectroscopic observations.
        model : nacl.models.salt.SALT2Like
            Model.
        """
        self.training_dataset = tds
        self.data = tds.spectrophotometric_data
        self.model = model

        self.spec_index = self.data.spec_index
        self.sn_index = self.data.sn_index
        self.z = self.data.z

        # Look at that later
        self.color_law = model.color_law
        self.pars = model.pars
        self.basis = model.basis

        self.wl_basis_size = len(model.basis.bx)
        self.ph_basis_size = len(model.basis.by)

        # restframe wavelengths
        self.restframe_wl = self.data.wavelength/(1.+self.z)
        #        self.Jl = model.basis.bx.eval(self.restframe_wl).tocsr()

        # and we can connect directly to the global parameters
        self.M0 = model.pars['M0'].full
        self.M1 = model.pars['M1'].full
        self.cl_pars = model.pars['CL'].full

    def __call__(self, jac=False, debug_mode=False):
        r"""
        Evaluate the model for a all spectra

        Parameters
        ----------
        jac : bool
            if True compute and return the jacobian matrix
        debug_mode : bool
            if true, just return the model components.

        Returns
        -------
        val : numpy.array
            Model evaluations.
        jacobian : scipy.sparse.csr_matrix
            Jacobian matrix (if jac is true).
        """

        t0 = time.perf_counter()
        pars = self.pars

        # sn-related parameters
        x0, x1 = pars['X0'].full[self.sn_index], pars['X1'].full[self.sn_index]
        c, tmax = pars['col'].full[self.sn_index],  pars['tmax'].full[self.sn_index]
        # c, tmax = pars['col'].full[self.sn_index],  pars['tmax'].full[self.training_dataset.spectrophotometric_data.isn]

        # we need to re-evaluate the basis on the phases, since tmax changes
        restframe_phases = (self.data.mjd-tmax)/(1.+self.z)
        jacobian = self.basis.eval(self.restframe_wl, restframe_phases + self.model.delta_phase).tocsr()

        # norm
        norm = self.model.norm

        # model components
        component_0 = jacobian.dot(self.M0)
        component_1 = jacobian.dot(self.M1)

        polynome_color_law, jacobian_color_law = self.color_law(self.restframe_wl, self.cl_pars, jac=jac)
        color_law = np.power(10., 0.4*c*polynome_color_law)
        zz = 1. + self.z

        pca = (component_0 + x1 * component_1)
        model = x0 * norm * pca * color_law / zz

        if debug_mode:
            return component_0, component_1, color_law, recal, model

        self.model.val.append(model)
        if not jac:
            self.model.timing.append(time.perf_counter()-t0)
            return model

        jacobian = jacobian.tocoo()
        # jacobian_spec_rec = jacobian_spec_rec.tocoo()

        jacobian_i, jacobian_j, jacobian_val = self.model.jacobian_i, self.model.jacobian_j, self.model.jacobian_val
        jacobian_i.append(self.data.row)
        jacobian_j.append(self.model.pars['X0'].indexof(self.sn_index))
        # jacobian_val.append((component_0 + x1*component_1) * color_law * recal / zz)
        jacobian_val.append(norm * pca * color_law / zz)

        # dMdX1
        # jacobian_i, jacobian_j, jacobian_val = self.model.jacobian_i, self.model.jacobian_j, self.model.jacobian_val
        jacobian_i.append(self.data.row)
        jacobian_j.append(self.model.pars['X1'].indexof(self.sn_index))
        # jacobian_val.append(x0 * component_1 * color_law * recal / zz)
        jacobian_val.append(x0 * norm * component_1 * color_law / zz)

        # dMdc
        jacobian_i.append(self.data.row)
        jacobian_j.append(self.model.pars['col'].indexof(self.sn_index))
        jacobian_val.append(model * 0.4 * np.log(10.) * polynome_color_law)

        # dMdtmax
        # we can gain a little here, by not evaluating the gradient along the wavelength (ddlambda)
        _, deval_phase = self.model.basis.gradient(self.restframe_wl, restframe_phases + self.model.delta_phase)
        deval_phase = deval_phase.tocsr()
        jacobian_i.append(self.data.row)
        jacobian_j.append(self.model.pars['tmax'].indexof(self.sn_index))
        #jacobian_val.append(-1. *x0* (deval_phase.dot(self.M0) + x1*deval_phase.dot(self.M1)) * color_law * recal / zz**2)
        jacobian_val.append(-1. * x0 * norm * (deval_phase.dot(self.M0) + x1*deval_phase.dot(self.M1)) * color_law / zz**2)

        # dmdtheta_0
        jacobian_i.append(self.data.row[jacobian.row])
        jacobian_j.append(self.model.pars['M0'].indexof(jacobian.col))
        #jacobian_val.append(x0[jacobian.row] *jacobian.data * color_law[jacobian.row] * recal[jacobian.row] / zz[jacobian.row])
        jacobian_val.append(x0[jacobian.row] * norm * jacobian.data * color_law[jacobian.row] / zz[jacobian.row])

        # dmdtheta_1
        jacobian_i.append(self.data.row[jacobian.row])
        jacobian_j.append(self.model.pars['M1'].indexof(jacobian.col))
        #jacobian_val.append(x0[jacobian.row]*x1[jacobian.row] * jacobian.data * color_law[jacobian.row] *
        #                    recal[jacobian.row] / zz[jacobian.row])
        jacobian_val.append(x0[jacobian.row] * x1[jacobian.row] * norm *  jacobian.data * color_law[jacobian.row]/ zz[jacobian.row])

        # dMdcl (color law)
        jacobian_color_law = scipy.sparse.coo_matrix(jacobian_color_law)
        jacobian_i.append(self.data.row[jacobian_color_law.row])
        jacobian_j.append(self.model.pars['CL'].indexof(jacobian_color_law.col))
        jacobian_val.append(c[jacobian_color_law.row] * 0.4 * np.log(10.) * jacobian_color_law.data *
                            model[jacobian_color_law.row])

        if self.model.disable_cache:
            self.model.clear_cache()
        self.model.timing.append(time.perf_counter()-t0)


        return model


class SALT2Eval:
    """Evaluate the model, for one single SN
    """
    def __init__(self, model, bands=['SWOPE::B'],
                 n_spectra=1, n_phot_spectra=1):
        """
        """
        self.orig_model = model
        self.phase_range = model.phase_range
        self.wl_range = model.wl_range
        self.tds = SimTrainingDataset(bands,
                                      n_spectra=n_spectra,
                                      n_phot_spectra=n_phot_spectra)
        # it is essential that the model is an exact duplicate
        # of the original model - just 1 SN instead of many
        self.model = model.clone(self.tds)

    # def clone_model(self):
    #     """instantiate a duplicate of the original model

    #     .. note :: a model should be able to clone itself - would be cleaner
    #     """
    #     model = self.orig_model
    #     ret = \
    #         SALT2Like(self.tds,
    #                   phase_range=model.phase_range,
    #                   wl_range=model.wl_range,
    #                   basis_knots=model.basis_knots,
    #                   basis_filter_knots=model.basis_filter_knots,
    #                   spectrum_recal_degree=model.spectrum_recal_degree,
    #                   normalization_band_name=model.normalization_band_name,
    #                   calib_variance=model.calib_variance)
    #     return ret

    def set(self, **kwargs):
        """initialize the sn parameters

        This function updates the dataset, and then the model
        parameters.
        """
        # sn parameters
        if 'z' in kwargs:
            z = kwargs.get('z')
            self.tds.sn_data.nt['z'] = z
            if self.tds.lc_data:
                self.tds.lc_data.z[:] = z
            if self.tds.spec_data:
                self.tds.spec_data.z[:] = z
            if self.tds.spectrophotometric_data:
                self.tds.spectrophotometric_data.z[:] = z
        if 'x0' in kwargs:
            self.tds.sn_data.nt['x0'] = kwargs['x0']
        if 'x1' in kwargs:
            self.tds.sn_data.nt['x1'] = kwargs['x1']
        if 'col' in kwargs:
            self.tds.sn_data.nt['col'] = kwargs['col']
        if 'tmax' in kwargs:
            tmax = kwargs['tmax']
            self.tds.sn_data.nt['tmax'] = kwargs['tmax']
            if self.tds.lc_data:
                self.tds.lc_data.nt['mjd'] = self.tds.mjd +tmax
        if 'ebv' in kwargs:
            self.tds.sn_data.nt['ebv'] = kwargs['ebv']

        if 'spec_mjd' in kwargs:
            if self.tds.spec_data:
                self.tds.spec_data.nt['mjd'] = kwargs['spec_mjd']
            if self.tds.spectrophotometric_data:
                self.tds.spectrophotometric_data.nt['mjd'] = kwargs['spec_mjd']

        # light curve zero points and magsys
        if 'zp' in kwargs:
            zps = kwargs['zp']
            for band_name in zps:
                idx = self.tds.lc_data.band == band_name
                self.tds.lc_data.nt['zp'] = zps[band_name]
        if 'magsys' in kwargs:
            magsys = kwargs['magsys']
            if type(magsys) is str:
                self.tds.lc_data.nt['magsys'][:] = magsys
            for band_name in magsys:
                idx = self.tds.lc_data.magsys == band_name
                self.tds.lc_data.nt['magsys'] = magsys[band_name]

        # recompute the photometric norm factors
        self.tds.compute_photometric_norm_factors()
        # propagate this into the model parameters
        self.model = self.orig_model.clone(self.tds)
        self.model.init_from_training_dataset()

    def set_from_tds(self, sn, tds):
        """load the sn parameters from a training dataset
        """
        sn_pars = tds.get_sn_pars(sn)
        if self.tds.lc_data:
            sn_pars['zp'] = tds.get_zp(sn)
            sn_pars['magsys'] = tds.get_magsys(sn)
        self.set(**sn_pars)
        # self.set(z=sn_pars['z'], x0=sn_pars['x0'],
        #          x1=sn_pars['x1'], col=sn_pars['col'],
        #          tmax=sn_pars['tmax'], ebv=sn_pars['ebv'],
        #          zp=zp, magsys=magsys)

    def update_global_pars(self, pars):
        """
        """
        for block_name in ['M0', 'M1', 'CL']:
            self.orig_model.pars[block_name].full[:] = pars[block_name].full[:]
            self.model.pars[block_name].full[:] = pars[block_name].full[:]

    def __call__(self):
        """evaluate the model and update the dataset with the model values

        This is the simplest way to evaluate the model.
        No need to clone the dataset or anything.
        """
        v = self.model(self.model.pars.free)
        self.tds.update_flux(v)

    def bandflux(self, bands, mjds, zp, zpsys):
        """evaluate the model for the requested bands and at the requested mjds

        This one in a little more costly, as we need to instantiate
        a new training dataset and re-instantiate a model.
        """
        pass

    def bandmag(self, bands, mjd, magsys):
        """return mags for the requested bands and at the requested mjds

        This is also a little more costly, as we need to instantiate
        a new training dataset and re-instantiate a model.
        """
        pass

    def spectrum(self, mjd):
        """evaluate and return a spectrophotometric spectrum
        """
        pass

    def photspectrum(self, mjd):
        """evaluate and return a spectrophotometric spectrum
        """
        pass

    def color_law(self, col=None):
        pass


# def main():
#     model = ...
#     m = SALT2LikeEval(model, bands=['SWOPE::B'])

#     # evaluate the model on all the data for this SN
#     # with the default parameters
#     m.eval(sn=sn)

#     # evaluate the model on all the data for this SN
#     # with alternative parameters
#     m.eval(sn=sn, sn_pars=sn_pars, model_pars=model_pars)

