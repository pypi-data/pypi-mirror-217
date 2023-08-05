"""

TODO: Put the iterative training steps.
"""
import numpy as np
import os
from .lib import bspline
from .minimizers import Minimizer, ModelPulls
from .models.constraints import Constraints2D
from .models.regularizations import SplineRegul2D
from .models.variancemodels import SimpleVarianceModel
from nacl import minimize
from nacl.models.regularizations import NaClSplineRegularization
from nacl.models.constraints import SALT2LikeConstraints, ab_flux_at_10Mpc

from .plotting import plots

try:
    from sksparse.cholmod import cholesky_AAt
except ImportError:
    from scikits.sparse.cholmod import cholesky_AAt



def fit(model, block_names, init_pars=None,
        reg_order=0, mu_reg=1.E-6, active_cons=None, mu_cons=1.E6,
        Mb=-19.5, n_iter=100):
    """
    """
    model.pars.fix()
    for block_name in block_names:
        model.pars[block_name].release()

    # we may need some regularization
    reg = []
    to_regularize = []
    for block_name in ['M0', 'M1']:
        if block_name in block_names:
            to_regularize.append(block_name)
    if len(to_regularize) > 0:
        reg = NaClSplineRegularization(model, to_regularize=to_regularize,
                                       order=reg_order, mu=mu_reg)
        reg = [reg]

    # we may need some contraints
    cons = []
    active = {}
    for cons_name in ['M0', 'dM0', 'M1', 'dM1', 'col', 'X1', 'X1_var']:
        if 'M0' in block_names and 'X0' in block_names:
            active['M0'] = ab_flux_at_10Mpc(Mb)
        if 'M1' in block_names:
            active['M1'] = 0.
        if 'M0' in block_names and 'tmax' in block_names:
            active['dM0'] = 0.
        if 'M1' in block_names and 'tmax' in block_names:
            active['dM1'] = 0.
        if 'CL' in block_names and 'col' in block_names:
            active['col'] = 0.
        if 'X1' in block_names and 'M1' in block_names:
            active['X1'] = 0.
            active['X1_var'] = 1.
    if len(active) > 0:
        cons = [SALT2LikeConstraints(model, active=active, mu=mu_cons)]

    # if there are constraints, make sure that they are fullfilled
    # at first order
    model.pars['X1'].full -= model.pars['X1'].full.mean()
    model.pars['X1'].full /= model.pars['X1'].full.std()
    model.pars['col'].full -= model.pars['col'].full.mean()

    # fit
    wres = minimize.WeightedResiduals(model)
    chi2 = minimize.LogLikelihood(wres, reg=reg, cons=cons)
    minz = minimize.Minimizer(chi2, n_iter=n_iter)

    # start the fit
    solution = minz.minimize(model.pars.free)

    ret = {}
    ret['solution'] = solution
    ret['model'] = model
    ret['cons'] = cons
    ret['reg'] = reg
    ret['chi2'] = chi2
    ret['pars'] = model.pars.copy()

    return ret


class FitModel2D(object):
    """
    Fitting procedure class.
    From a simulation, a model, error models, and parameters,
    can fit the model (given a minimizer) on data.
    If parameters are fixed, regularization and constraints are adjusted.

    All the parameters of the fit, amplitude of constraints, regularization can be specified.

    Attributes
    ----------
    training_dataset : nacl.dataset.TrainingDataset
        Training dataset.
    model : nacl.salt
        Model.
    gamma_init : numpy.array ou float
        Parameters used to initialize the error snake.
    basis_knot : 2-list
        Number of wavelength and photometric knot.
    init_from_salt2_file : str
        If the model is to be initialized with the original
        SALT2-4 surfaces and bases, get them from this file.
    norm_band : str
        Use this band to normalize the model.
    degree : int
        Degree of the spectrum recalibration polynomials
    BETA : float
        Diagonal offset in hessian matrix where use of cholesky.
    queue_wsp : list
        Model queue of eval unit.
    pars_free : list
        List of free parameters in the fit.
    beta : numpy.array
        Fitted model parameter.
    beta0 : numpy.array
        Model parameter initialization.
    reg : nacl.models.regularizations
        Class of regularization.
    pars_generation : numpy.array
        Parameters used for the simulation.
    all_pars : list
        List of all the parameters of the model.
    cons : nacl.models.constraints
        Class of constraints.
    x1_var_real : float
        Amplitude of constraints to the total :math:`\chi^2`
    N_sn_4plot : int
        Index of SN data to plot.
    variance_model : nacl.models.variancemodels.SimpleVarianceModel
        Error snake model.
    gamma : numpy.array
        Fitted error snake parameter :math:`\gamma`
    gamma0 : numpy.array
        Error snake parameter :math:`\gamma` at initialisation
    kappa_init : numpy.array
        Color scatter parameters.
    color_scatter_func : object
        Color scatter function used.
    color_scatter : nacl.models.variancemodels.ColorScatter
        Color scatter model.
    mu_pq : float
        Amplitude of the linear constraints to the total :math:`\chi^2`.
    log : list
        For debugging reason, stored at each step all fit quantities.
    N_ITER : int
        Maximum number of fit iteration.
    df_stop : float
        :math:`\Delta \chi^2` after which the fit stops.
    pars_fix : list
        List a parameter fixed during the fit.
    mu_pq_var_x1 : float
        Amplitude of constraints on :math:`X_1` variance to the total :math:`\chi^2`
    mu_reg : float
        Amplitude of the regularization to the total :math:`\chi^2`
    chi2_normalization : float
        Ratio of :math:`\chi^2` of spectral data and :math:`\chi^2` of photometric data.
    minimize_func : nacl.minimizers.Minimizer
        Minimizer.
    log : list
        For debugging reason, stored at each step all fit quantities.
    df_stop : float
        :math:`\Delta \chi^2` after which the fit stops.
    pars_fix : list
        List a parameter fixed during the fit.

    """
    def __init__(self, training_dataset, model_func, normalization_band_name='SWOPE::B',
                 init_from_salt2_file='data/salt2.npz', pars_fix=[],
                 minimizer=Minimizer, degree=3, disconnect_sp=False,
                 gamma_init=0.05, kappa_init=None, x1_var_real=False,
                 mu_pq=1e10, mu_pq_var_x1=None, mu_reg=1,
                 variance_model_bins=(3,3),
                 chi2_normalization=1, color_scatter_func=None, beta=1e-10,
                 log=True, df_stop=1e-1, n_iter=500, basis_knots=[127, 20],
                 pars_generation=None):
        """
        Constructor.

        Parameters
        ----------
        training_dataset : nacl.dataset.TrainingDataset
            Training dataset.
        model_func : nacl.salt
            Model.
        gamma_init : numpy.array ou float
            Parameters used to initialize the error snake.
        basis_knots : 2-list
            Number of wavelength and photometric knot.
        init_from_salt2_file : str
            If the model is to be initialized with the original
            SALT2-4 surfaces and bases, get them from this file.
        normalization_band_name : str
            Use this band to normalize the model.
        degree : int
            Degree of the spectrum recalibration polynomials
        beta : float
            Diagonal offset in hessian matrix where use of cholesky.
        pars_generation : numpy.array
            Parameters used for the simulation.
        x1_var_real : float
            Amplitude of constraints to the total :math:`\chi^2`
        N_sn_4plot : int
            Index of SN data to plot.
        kappa_init : numpy.array
            Color scatter parameters.
        color_scatter_func : nacl.models.variancemodels.ColorScatter
        mu_pq : float
            Amplitude of the linear constraints to the total :math:`\chi^2`.
        log : list
            For debugging reason, stored at each step all fit quantities.
        n_iter : int
            Maximum number of fit iteration.
        df_stop : float
            :math:`\Delta \chi^2` after which the fit stops.
        pars_fix : list
            List a parameter fixed during the fit.
        mu_pq_var_x1 : float
            Amplitude of constraints on :math:`X_1` variance to the total :math:`\chi^2`
        mu_reg : float
            Amplitude of the regularization to the total :math:`\chi^2`
        variance_model_bins : tuple(int, int)
            Number of bins of the vraince surface
        chi2_normalization : float
            Ratio of :math:`\chi^2` of spectral data and :math:`\chi^2` of photometric data.
        minimizer : nacl.minimizers.Minimizer
            Minimizer.
        log : list
            For debugging reason, stored at each step all fit quantities.
        df_stop : float
            :math:`\Delta \chi^2` after which the fit stops.
        pars_fix : list
            List a parameter fixed during the fit.

        """
        self.training_dataset = training_dataset
        self.norm_band = normalization_band_name
        self.degree = degree
        self.BETA = beta
        self.gamma_init = gamma_init
        self.kappa_init = kappa_init
        self.color_scatter_func = color_scatter_func
        self.x1_var_real = x1_var_real

        self.pars_free, self.x0, self.g0, self.reg, self.cons = None, None, None, None, None

        self.basis_knots = basis_knots
        self.model = model_func(self.training_dataset,
                                normalization_band_name=self.norm_band,
                                spectrum_recal_degree=self.degree,
                                basis_knots=self.basis_knots)

        self.queue_wsp = self.model.queue.copy()

        self.init_model_pars(filename=init_from_salt2_file, sn_info=self.training_dataset.sn_data)

        self.variance_model = SimpleVarianceModel(self.model,
                                                  gamma_init=self.gamma_init,
                                                  bins=variance_model_bins)

        self.pars_generation = pars_generation
        self.N_sn_4plot = None
        self.all_pars = ['X0', 'tmax', 'X1', 'col', 'M0', 'M1', 'CL',
                         'SpectrumRecalibration', 'eta_calib', 'kappa_color']

        self.mu_pq = mu_pq
        self.mu_pq_var_x1 = mu_pq_var_x1
        self.mu_reg = mu_reg
        self.chi2_normalization = chi2_normalization
        self.minimize_func = minimizer

        self.log = log
        self.N_ITER = n_iter
        self.df_stop = df_stop

        self.pars_fix = pars_fix
        self.pars_release()
        self.model.pars0 = self.model.pars.full[:].copy()


    def init_model_pars(self, filename, sn_info):
        r"""
        Initiate model parameters.

        Parameters
        ----------
        filename : str
            The original
            SALT2-4 surfaces and bases, get them from this file.
        sn_info : numpy.rec.array
            SNe information (:math:`(z, X_0, X_1, c, t_{max})`)
        """
        m0, m1, cl = self.init_with_salt2(filename, self.model)

        self.model.pars['X0'][:] = sn_info.x0
        self.model.pars['X1'][:] = sn_info.x1
        self.model.pars['tmax'][:] = sn_info.tmax
        self.model.pars['col'][:] = sn_info.col

        self.model.pars['M0'][:] = m0
        self.model.pars['M1'][:] = m1
        self.model.pars['CL'][:] = cl
        self.model.norm = self.model.normalization(band_name=self.norm_band)

    @staticmethod
    def init_with_salt2(filename, model):
        """
        Initiate the model with salt2.4 files.

        Parameters
        ----------
        filename : str
            The original SALT2-4 file.
        model : nacl.models.salt.SALT2Like
            Model.
        """
        f = np.load(filename)
        phase_grid = f['phase_grid']
        wl_grid = f['wl_grid']
        basis = bspline.BSpline2D(wl_grid, phase_grid, x_order=4, y_order=4)

        xx = np.linspace(wl_grid[0], wl_grid[-1], basis.bx.nj)
        yy = np.linspace(phase_grid[0], phase_grid[-1], basis.by.nj)

        x, y = np.meshgrid(xx, yy)
        x, y = x.ravel(), y.ravel()
        jacobian = model.basis.eval(x, y)
        factor = cholesky_AAt(jacobian.T, beta=1e-20)

        return factor(jacobian.T * f['M0']), factor(jacobian.T * f['M1']), f['CL_pars']

    def pars_release(self):
        """
        Fixed the parameters label a pars_fix.
        """
        self.pars_free = [i for i in self.all_pars if i not in self.pars_fix]
        self.model.pars.fix()
        for pr in self.pars_free:
            self.model.pars.release(pr)

    def parameter_degradation(self, model_coef_init=0.05,
                              var_coef_init=0.1,
                              seed=None):
        """
        Degrade the parameters.
        Multiply their values by normal distribution, of mean 1 and a chosen standard deviations.
        For :math:`t_{max}` add normal distribution, of mean 0 and a chosen standard deviations.

        Parameters
        ----------
        model_coef_init : float
            Standard deviation for the model parameters : :math:`(X_0, X_1, c, t_{max})`
        var_coef_init : float
            Standard deviation for the error snake parameters : :math:`\gamma`
        seed : int
            Seed for numpy.random
        """
        if seed is not None:
            np.random.seed(seed)

        self.variance_model.pars.full[:] *= np.random.normal(1., var_coef_init,
                                                             len(self.variance_model.pars.full))
        print(f'\nVarModPars times N(1, {var_coef_init})')
        nb_sn = len(self.model.training_dataset.sne)
        for ps in self.pars_free:
            if (ps != 'eta_calib') & (ps != 'tmax'):
                mv = model_coef_init
                self.model.pars[ps].full[:] *= np.random.normal(1., mv,
                                                                len(self.model.pars[ps].full))
                if ps == 'X1':
                    self.model.pars[ps].full[:] -= self.model.pars[ps].full[:].mean()

                print(f'{ps} times N(1, {mv})')

            elif model_coef_init != 0.:
                if ps == 'tmax':
                    s_tmax = 0.05
                    self.model.pars['tmax'].full[:] += np.random.normal(0, s_tmax, nb_sn)
                    print(f'{ps} + N(0, {s_tmax})')
        print('\n')
        self.gamma0 = self.variance_model.pars.free.copy()
        self.beta0 = self.model.pars.free.copy()

    def regularization(self, sur_reg=np.array(['M0', 'M1'])):
        """
        Instantiate regularization class.

        Parameters
        ----------
        sur_reg : numpy.array
            Surfaces to regularized.
        """
        sur_id = np.in1d(sur_reg, self.pars_free)
        if sur_id.sum() != 0:
            print(f'reg : {sur_reg[sur_id]}')
            self.reg = SplineRegul2D(self.model, mu=self.mu_reg,
                                     surfaces_reg=sur_reg[sur_id])
        else:
            self.reg = None

    def constraints(self, paramaters_cons=np.array(['M0', 'M1', 'CL', 'X0', 'tmax', 'X1', 'c'])):
        """
        Instantiate regularization class.

        Parameters
        ----------
        paramaters_cons : numpy.array
            List of parameters on which a constraint is applied.
        """
        cons_id = np.in1d(paramaters_cons, self.pars_free)

        # if model is fixed no need of contains
        if np.in1d(np.array(['M0', 'M1', 'CL']), self.pars_fix).sum() != 0.:
            self.cons = None

        elif cons_id.sum() != 0:
            cc = [i for i in paramaters_cons[cons_id]]
            print(f'cons : {cc}')
            self.cons = Constraints2D(self.model, mu_pq=self.mu_pq, parameters_cons=cc,
                                      mu_pq_var_x1=self.mu_pq_var_x1,
                                      x1_var_real=self.x1_var_real)   # ,vals = [])

        else:
            self.cons = None

    def __call__(self, pars_fix=[],
                 g=None, eta_covmatrix=None, sigma_kappa=None,
                 fit_spec=True, sigma_kappa_fit=True):
        """
        Fit !

        Parameters
        ----------
        pars_fix : list
            List of fixed parameters during the fit. If the error snake should
            be fixed 'gamma' should appear here.
        g : np.array
            Error snake parameters free or fixed.
        eta_covmatrix : float or numpy.array
            Calibration uncertainty matrix.
        sigma_kappa :
            Color scatter parameter.
        fit_spec : bool
            If spectral data are considered.
        sigma_kappa_fit : bool
            If color scatter should be fixed.

        TODO : add color scatter parameters fixation in pars_fix.
        """

        self.pars_fix = np.array(pars_fix)
        self.pars_release()

        print("\nNumber of free parameters :")
        for i in self.all_pars:
            print(i, self.model.pars[i].free.shape)
        print("\n")

        self.regularization()
        self.constraints()
        self.g = g
        if fit_spec is False:
            self.model.queue = [i for i in self.model.queue if (i.data['spec_id'].mean() == -1)]

        self.f = ModelPulls(self.model,
                            variance_model=self.variance_model, fit_spec=fit_spec,
                            chi2_normalization=self.chi2_normalization)

        if 'gamma' in pars_fix:
            self.f.VarianceModel.pars.fix()

        if sigma_kappa is not None:
            self.color_scatter = self.color_scatter_func(self.model.lambda_c_red, sigma_kappa)
        else :
            self.color_scatter = None

        minimizer = self.minimize_func(self.f, constrains=self.cons,
                                       regularization=self.reg,
                                       color_scatter=self.color_scatter, ##
                                       n_iter=self.N_ITER,
                                       df_stop=self.df_stop, log=self.log, beta_cholmod=self.BETA)

        minimizer(self.model.pars.free, sigma_kappa=sigma_kappa,
                  gamma0=self.g, eta_covmatrix=eta_covmatrix, sigma_kappa_fit=sigma_kappa_fit)

        self.M = minimizer.M
        self.gradf = minimizer.gradf
        self.minim = minimizer

        self.sigma_kappa = minimizer.sigma_kappa
        if (self.sigma_kappa is not None) & sigma_kappa_fit:
            self.dsigma_kappa = minimizer.dsigma_kappa

        self.timing = {'iter': np.array(minimizer.titer).mean(),
                       'cholesky': np.array(minimizer.tcholesky).mean(),
                       'model': np.array(minimizer.tmodel).mean(),
                       'hessian': np.array(minimizer.thessian).mean(),
                       's_iter': np.array(minimizer.titer).std(),
                       's_cholesky': np.array(minimizer.tcholesky).std(),
                       's_model': np.array(minimizer.tmodel).std(),
                       's_hessian': np.array(minimizer.thessian).std()}

        self.log = minimizer.log

        self.beta = minimizer.beta
        self.gamma = minimizer.gamma

        if fit_spec is False:
            self.model.queue = self.queue_wsp

    def control_plot(self, n_fit, variance_model=None,
                     theta_init=None, save_dir=None, add_name=''):
        """
        Make control plots.
        """
        if save_dir is not None:
            save_dir = f'{save_dir}'
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

        if variance_model is not None:
            variance_model = self.variance_model
        if self.N_sn_4plot is None:
            self.N_sn_4plot = np.random.randint(0, len(self.training_dataset.sne), 5)

        for isn in self.N_sn_4plot:
            plots.plot_lc(self.model, isn, variance_model=variance_model,
                          save_dir=save_dir, add_name=add_name)
            plots.plot_spec(self.model, isn, variance_model=variance_model,
                            save_dir=save_dir, add_name=add_name)
        # plots.binning_residuals(self.model, save_dir=save_dir, add_name=add_name)
        plots.residual_histogram(self.model, n_fit, variance_model=variance_model,
                                 data_selection=False, save_dir=save_dir)

        if variance_model:
            plots.plot_2Dsurfacemodel(variance_model, ['gamma'],
                                      vmin=0.90, vmax=1.1, ddd=False,
                                      init_unit=True, theta_init=theta_init,
                                      save_dir=save_dir, add_name=add_name)
