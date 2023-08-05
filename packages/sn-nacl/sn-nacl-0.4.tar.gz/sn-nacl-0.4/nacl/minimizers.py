"""
This module contains the Newton Raphson minimizer use in NaCl.
It is a minimizer of a log likelihood function.
This function is composed of different pieces :
 - a non-linear model;
 - a set of contains;
 - regularization;
 - variance models : Error Snake and Color Scatter;
 - calibration propagation term.
"""


import numpy as np
import scipy.sparse
from scipy.sparse import coo_matrix, csc_matrix
from sksparse import cholmod
import time
import logging
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG)


class Minimizer(object):
    r"""
    Newton Raphson minimizer.

    Iterative algorithm that calculates for each iteration the increment :math:`\delta \beta`:

    .. math :: \delta \beta = -H^{-1} \nabla \chi^2

    where :math:`\chi^2` is :math:`-2 \log(L)` and implemented in the Chi2Model class,
    :math:`\nabla \chi^2` is the gradient and :math:`H` is the hessian.

    Attributes
    ----------
    pull_function : ModelPulls
        Class of pull evaluation, difference of model and data, on variance model.
        If no variance model is considered, the denominator is the 'FluxErr' of the data.
    constrains : Constraints2D
        Class of constraints, evaluating the constraint as a function of the free parameters of the model.
    regularization : SplineRegul2D
        Class of regularization term, constraints splines parameters of surfaces without data.
    log : list
        Debug to keep in memory at each iteration all useful information,
        :math:`\beta, d\beta, \gamma, d\gamma, \chi^2(\beta), \chi^2(\beta+d\beta)`
    beta_cholmod : float
        Term in order to get the hessian positive definite (odg :math:`\sim 10^{-10}`)
    N_ITER : int
        Number of iteration maximum, after which the fit stops.
    DF_STOP :
        Threshold of :math:`\Delta \chi^2` that defines the convergence.
    lambda_c : array
        Mean rest-frame wavelength of each Light Curve.
    lambda_c_red :
        Reduced mean rest-frame wavelength of each Light Curve.
    beta : array
        Iteration model parameters.
    gamma : array
        Iteration variance model parameters.
    dbeta : array
        Iteration increment on model parameters.
    dgamma : array
        Iteration increment on variance model parameters.
    dsigma_kappa : array
        Increment on color scatter parameters.
    decrement : float
        Iteration :math:`\Delta \chi^2`
    hess : coo_matrix
        Iteration hessian matrix of the :math:`\chi^2`
    grad : array
        Iteration gradient of the :math:`\chi^2`
    increment : array
        increment
    """

    def __init__(self, pull_function,
                 constrains=None, regularization=None, color_scatter = None,
                 n_iter=1000,
                 df_stop=1e-5, log=None, beta_cholmod=1e-10):
        r"""
        Initiate the Minimizer class :

        Parameters
        ----------
        pull_function : ModelPulls
            Class of pull evaluation, difference of model and data, on variance model.
            If no variance model is considered, the denominator is the 'FluxErr' of the data.
        constrains : Constraints2D
            Class of constraints, evaluating the constraint as a function of the free
            parameters of the model.
        regularization : SplineRegul2D
            Class of regularization term, constraint splines parameters of surfaces without data.
        color_scatter :  ColorScatter
            Color scatter function that evaluate the color scatter and its derivatives.
        n_iter : int
            Number of iteration maximum, after which the fit stops.
        df_stop : float
            Threshold of :math:`\Delta \chi^2` that defines the convergence.
        log : bool
            Debug to keep in memory at each iteration all useful information,
            :math:`\beta, d\beta, \gamma, d\gamma, \chi^2(\beta), \chi^2(\beta+d\beta)`
        beta_cholmod : float
            Term in order to get the hessian positive definite (odg :math:`\sim 10^{-10}`)
        """
        self.pull_function = pull_function
        self.constrains = constrains
        self.regularization = regularization
        self.color_scatter = color_scatter
        self.log = log

        self.beta_cholmod = beta_cholmod
        self.N_ITER = n_iter
        self.DF_STOP = df_stop

        if self.log is not None:
            self.log = []

        self.lambda_c = self.pull_function.model.lambda_c
        self.lambda_c_red = self.pull_function.model.lambda_c_red
        self.beta, self.gamma, self.dbeta, self.dgamma, self.dsigma_kappa = None, None, None, None, None
        self.decrement = None
        self.hess, self.grad, self.increment = None, None, None

    def log_append(self, iteration, chi2_1, f_val, detail1, detail2):
        r"""
        Add to log the information of the iteration.

        Parameters
        ----------
        iteration : int
            Iteration number.
        chi2_1 : float
            :math:`\chi^2(\beta_{iteration - 1})`
        f_val : float
            :math:`\chi^2(\beta_{iteration})`
        detail1 : dict
            Values of the different component of the  :math:`\chi^2`, of the iteration number : iteration - 1
        detail2 : dict
            Values of the different component of the  :math:`\chi^2` of the iteration number : iteration
        """
        if self.log is not None:
            if self.sigma_kappa_fit & (self.sigma_kappa is not None):
                self.log.append((iteration, self.beta, self.gamma, self.dgamma, self.dbeta,
                                 chi2_1, f_val, self.M, detail1, detail2,
                                 self.sigma_kappa.copy(), self.dsigma_kappa))
            else:
                self.log.append((iteration, self.beta, self.gamma, self.dgamma, self.dbeta,
                                 chi2_1, f_val, self.M, detail1, detail2, None, None))

    def parameter_update(self):
        r"""
        Updated the values of the model parameters :math:`\beta` and the variances model parameters : :math:`\gamma`,
        :math:`\sigma_\kappa` for the considered iteration.

        Note
        ----
        In increment the parameters are stored as following :  :math:`(\beta, \gamma, \sigma_\kappa)`
        """
        if self.sigma_kappa_fit & (self.sigma_kappa is not None):
            # Slice the sigma_kappa parameters in increment
            self.dsigma_kappa = self.increment[self.fchi2.N_PAR:]
            # Slice the gamma parameters in increment
            self.dgamma = self.increment[len(self.beta): - len(self.dsigma_kappa)]
        else:
            self.dgamma = self.increment[len(self.beta):]

        self.dbeta = self.increment[: len(self.beta)]
        t = 1.

        self.beta = self.beta + t * self.dbeta

        if len(self.pull_function.VarianceModel.pars.free) != 0:
            self.gamma = self.gamma + t * self.dgamma
        if self.sigma_kappa_fit & (self.sigma_kappa is not None):
            self.sigma_kappa += t * self.dsigma_kappa
            print('sigma_kappa : ', self.sigma_kappa)
            print('dsigma_kappa : ', self.dsigma_kappa)

    def print_end_iter(self, t, chi2_1, f_val, n_dof, detail1, detail2):
        r"""
        Print the iteration information of the :math:`\chi^2`.

        Parameters
        ----------
        t : float
            Line-search parameters, default value is 1
        chi2_1 : float
            :math:`\chi^2(\beta_{iteration - 1})`
        f_val : float
            :math:`\chi^2(\beta_{iteration})`
        n_dof : float
            Number of degrees of freedom, calculated as the difference of the number
            of data point and the number of free parameters.
        detail1 : dict
            Values of the different component of the  :math:`\chi^2`, of the iteration number : iteration - 1
        detail2 : dict
            Values of the different component of the  :math:`\chi^2` of the iteration number : iteration
        """
        print('chi^2 contribution  i-1: ', detail1, '\n', 'chi^2 contribution  i: ',  detail2, '\n')
        if (np.isnan(f_val) ^ np.isinf(f_val)).sum() > 0:
            raise ValueError(f'Value of f_val : {f_val} ')
        self.decrement = chi2_1 - f_val
        logging.info('step size: %g, objective: %g -> %g, decrement: %g, D.o.F.: %d, objective/dof: %g'
                     % (t, chi2_1, f_val, self.decrement, n_dof, f_val/n_dof))
        print(f"t_tot : {self.titer[-1]},  t_cho : {self.tcholesky[-1]}")

    def __call__(self, beta0, sigma_kappa=None, gamma0=None, eta_covmatrix=None,
                 sigma_kappa_fit=True):
        r"""
        Find the parameters of the model and the variance model by minimizing the log likelihood function.

        Parameters
        ----------
        beta0 : array
            Initial model's parameters
        sigma_kappa : array or None
            Initial color scatter parameters.
            If None, the color scatter is not fitted.
            Kappa parameters of the model should be fixed, otherwise the degeneracy in the model is not broken.
        gamma0 :  array or None
            Initial error snake.
            If None, the variance of data is given by the square of the error on the measurement.
        eta_covmatrix : array or None
            Calibration zero point incertitude matrix.
            Eta parameters of the model should be fixed, otherwise the degeneracy in the model is not broken.
        sigma_kappa_fit : bool
           True : sigma kappa of fitted
           False : They are not, but if sigma_kappa is not None, kappa parameters are fitted, with a fix color scatter.
        """
        self.gamma0 = self.gamma = gamma0
        self.beta = self.beta0 = beta0.copy()
        self.n = len(beta0)

        self.factorCS = None

        self.sigma_kappa_fit = sigma_kappa_fit
        self.sigma_kappa = sigma_kappa

        if self.gamma0 is None:
            self.gamma = []

        self.M = np.ones(1)
        self.tcholesky, self.tmodel, self.thessian, self.titer = [], [],  [],  []
        for iteration in range(self.N_ITER):
            t0 = time.time()
            print('\n')
            logging.info('iteration: %d' % iteration)
            beta_keep = self.beta.copy()
            if len(self.gamma) != 0:
                gamma_keep = self.gamma.copy()
            hess_keep = self.M.copy()

            self.fchi2 = Chi2Model(pull_function=self.pull_function, constrains=self.constrains,
                                   regularization=self.regularization, color_scatter=self.color_scatter,
                                   sigma_kappa_fit=sigma_kappa_fit)

            chi2_1, detail1, self.gradf, self.M = self.fchi2(self.beta, self.gamma, self.sigma_kappa,
                                                             eta_covmatrix=eta_covmatrix,
                                                             derivatives=True)

            tmod = self.fchi2.model_evaluation
            thess = self.fchi2.hessian_construction
            self.thessian.append(thess)
            self.tmodel.append(tmod)

            # solve the normal equation
            t_cho = time.time()

            # When Error snake is fitted : M not positively definated
            # => should use mode=simplicial (much slower)
            # if len(self.pull_function.VarianceModel.pars.free) == 0:
            #     fact = cholmod.cholesky(self.M.tocsc(), mode='supernodal',
            #                             ordering_method='metis', beta=self.beta_cholmod)

            #     print('SUPERNODAL')
            # else :
            fact = cholmod.cholesky(self.M.tocsc(), mode='simplicial',
                                    ordering_method='metis', beta=self.beta_cholmod)
            print('SIMPLICIAL')

            self.tcholesky.append(time.time() - t_cho)
            self.increment = fact(-1*self.gradf)

            self.parameter_update()

            if self.constrains is not None:
                print('CHECK CONS 1: ', self.constrains(self.beta)*np.sqrt(self.constrains.sig_vals))
                print('Variance X1 : ', self.constrains.var_x1(self.beta)/np.sqrt(self.constrains.mu_pq_var_x1), '\n')

            ndof = len(self.pull_function.data) - len(self.beta)
            if len(self.pull_function.VarianceModel.pars.free) != 0:
                ndof -= len(self.gamma)

            if self.sigma_kappa_fit & (self.sigma_kappa is not None):
                ndof -= len(self.sigma_kappa)

            f_val, detail2 = self.fchi2(self.beta, self.gamma, self.sigma_kappa,
                                        eta_covmatrix=eta_covmatrix, derivatives=False)
            t = 1.
            self.titer.append(time.time() - t0)
            self.print_end_iter(t, chi2_1, f_val, ndof, detail1, detail2)
            self.log_append(iteration, chi2_1, f_val, detail1, detail2)

            self.iminus1_chi2 = chi2_1
            self.final_chi2 = f_val

            self.iter = iteration
            if self.decrement < 0.0:
                self.beta = beta_keep
                self.M = hess_keep
                if len(self.gamma) != 0:
                    self.gamma = gamma_keep
                if self.sigma_kappa_fit & (self.sigma_kappa is not None):
                    self.sigma_kappa = self.sigma_kappa - t * self.dsigma_kappa
                self.pull_function.model.pars.free = self.beta

                if len(self.pull_function.VarianceModel.pars.free) != 0:
                    self.pull_function.VarianceModel.pars.free = self.gamma

            if self.decrement < self.DF_STOP:
                break


class Chi2Model(object):
    r"""
     compute the full Lagrangian, including
      - the model,
      - Error snake
      - Color scatter
      - Constraints [optional]: a quadratic penalty derived from the constraints
      - Regularization [optional]
      - Propagation of calibration:

     .. math::
         \chi^{2} = \, & \chi^{2}_{model} + \chi^{2}_{cons} + \chi^{2}_{reg} +
         \chi^{2}_{calib} + \chi^{2}_{CS}  \nonumber \\
         =\, & \ln(|V(\beta, \gamma)|) + R(\beta)^T V^{-1}(\beta, \gamma) R(\beta) \nonumber \\
         + \, &  \mu_{pen} C(\beta)^T C(\beta) \nonumber \\
         +\, & \mu_{reg} \beta^T P \beta \nonumber \\
         + \, & \eta^T V^{-1}_{\eta} \eta \nonumber\\
         +\,& \ln{|V_{\kappa}( \sigma_\kappa)|} + \kappa^T V_\kappa^{-1}( \sigma_\kappa) \kappa


    Attributes
    ----------
    pull_function : ModelPulls
        Class of pull evaluation, difference of model and data, on variance model.
        If no variance model is considered, the denominator is the 'FluxErr' of the data.
    constrains : Constraints2D
        Class of constraints, evaluating the constraint as a function of the free parameters of the model.
    regularization : SplineRegul2D
        Class of regularization term, constraints splines parameters of surfaces without data.
    lambda_c : array
        Mean rest-frame wavelength of each Light Curve.
    lambda_c_red :
        Reduced mean rest-frame wavelength of each Light Curve.
    sigma_kappa_fit : bool
        Whether color scatter parameters are fitted.
    beta : array
        Model parameters.
    gamma : array
        Variance model parameters.
    hess : coo_matrix
        Hessian matrix of the :math:`\chi^2`
    grad : array
        Gradient of the :math:`\chi^2`
    hessian_construction : float
        Time of model part hessian matrix construction
    model_evaluation : float
        Time passing evaluating models
    """
    def __init__(self, pull_function, constrains=None,
                 regularization=None, color_scatter=None,
                 sigma_kappa_fit=True):
        """
        Initialization of the class.

        Parameters
        ----------
        pull_function : ModelPulls
            Class of pull evaluation, difference of model and data, on variance model.
            If no variance model is considered, the denominator is the 'FluxErr' of the data.
        constrains : Constraints2D
            Class of constraints, evaluating the constraint as a function of the free parameters of the model.
        regularization : SplineRegul2D
            Class of regularization term, constraints splines parameters of surfaces without data.
        color_scatter :  ColorScatter
            Color scatter function that evaluate the color scatter and its derivatives.
        sigma_kappa_fit : bool
            Whether color scatter parameters are fitted.

        """
        self.pull_function = pull_function
        self.regularization = regularization
        self.constrains = constrains
        self.color_scatter = color_scatter

        self.lambda_c_red = self.pull_function.model.lambda_c_red
        self.lambda_c = self.pull_function.model.lambda_c
        self.sigma_kappa_fit = sigma_kappa_fit
        self.hess, self.grad = None, None
        self.hessian_construction, self.model_evaluation = None, None

    def __call__(self, beta, gamma, sigma_kappa=None, eta_covmatrix=None, derivatives=False):
        r"""
        Evaluation of the :math:`\chi^2`, with the update parameters
        (math:`\beta`, math:`\gamma`, math:`\sigma_\kappa`).
        Evaluated the gradiant and the hessian if needed.

        Parameters
        ----------
        beta : array
           Model parameters.
        gamma : array
           Error snake parameters.
        sigma_kappa : array
           Color scatter parameters.
        eta_covmatrix : float or array
           Calibration uncertainty matrix.
        derivatives : bool
           If gradient and hessian are needed.

        Returns
        -------
        chi2 : float
             :math:`\chi^2` calculates with the update parameters
        detail : dict
             Component of the :math:`\chi^2`

        if derivatives :
        chi2 : float
             :math:`\chi^2` calculates with the update parameters
        detail : dict
             Component of the :math:`\chi^2`
        grad : array
             Gradient of the :math:`\chi^2`
        hess : scipy.sparse.csc_matrix
             Hessian of the :math:`\chi^2`
        """
        self.detail = {}
        self.beta, self.gamma = beta, gamma
        self.N_PAR = len(beta)
        self.rho = self.beta.copy()
        if self.pull_function.VarianceModel is not None and \
                len(self.pull_function.VarianceModel.pars.free) != 0:
            self.N_PAR += len(self.gamma)
            self.rho = np.hstack((self.rho, self.gamma))
        self.sigma_kappa = sigma_kappa
        self.chi2 = 0

        self.model_reg(derivatives=derivatives)
        if eta_covmatrix is not None:
            self.calibration_gaussian_prior(eta_covmatrix, derivatives=derivatives)
        if self.constrains is not None:
            self.get_constrains_derivatives(derivatives=derivatives)
        if sigma_kappa is not None:
            self.color_scatter_evaluation(derivatives=derivatives)
        if derivatives:
            return self.chi2, self.detail, self.grad, self.hess
        return self.chi2, self.detail

    def model_reg(self, derivatives=False):
        r"""
        - Compute the model and error snake contribution to the total :math:`\chi^2`,
        grouping all parameters under a single variable :

        .. math::
            \rho = \left( \begin{matrix}
            \beta \\
            \gamma \\
            \sigma_\kappa
            \end{matrix}\right)

        We get :

        .. math::
         \chi^2_{model} = \ln(|V(\rho)|) + R(\rho)^T  V^{-1}(\rho) R(\rho)

        For the gradient vector :

        .. math::
            \frac{\partial \chi^2_{model}(\rho)}{\partial \rho_i}  = Tr\left(V^{-1} J_{V,i} \right) -
            2 J_i^T V^{-1} R - R^T V^{-1} J_{V,i} V^{-1} R

        For the hessian matrix :

        .. math::
            H  = \frac{\partial^2 \chi^2_{model}(\rho)}{\partial \rho_i \partial \rho_j}= (H)_{ij} =
            \left( Tr\left( -V^{-1} J_{V,j} V^{-1} J_{V,i} \right) + 2  J_i^T V^{-1} J_j^T\right)_{ij}


        - Compute regularization component of the total :math:`\chi^2`:

        .. math::
            \chi^2_{reg} = \mu_{reg} \beta^T P \beta

        If derivatives are needed:
        adding to the total gradient :

        .. math::
            \frac{\partial \chi^2_{reg}(\beta)}{\partial \beta}  = \mu_{reg} \rho^T P

        and to the hessian matrix :

        .. math::
            \frac{\partial \chi^2_{reg}(\beta)}{\partial \beta \partial \beta} = 2 \mu_{reg} P


        Parameters
        ----------
        derivatives : bool
           If gradient and hessian are needed.
        """
        lower_triangular_matrix = None

        tmod = time.time()
        if derivatives:
            # if len(self.gamma) != 0.:
            pull, derivative_pull, val, jacobian, variance, \
                derivative_variance = self.pull_function(self.beta, gamma=self.gamma, jac=True)

        # else:
        # pull, derivative_pull, val, jacobian = self.pull_function(self.beta, jac=True)
        #        variance = self.pull_function.data['FluxErr']**2
        else:
            if len(self.gamma) != 0.:
                pull, val = self.pull_function(self.beta, gamma=self.gamma, jac=False)
            else:
                pull, val = self.pull_function(self.beta, jac=False)
        self.model_evaluation = time.time() - tmod
        # this is ugly. We're not supposed to know the internals
        # of the pull function here - rewrite
        # res = self.pull_function.data['Flux'] - val
        res = self.pull_function.flux - val
        pull_tilde = pull

        if self.regularization is not None:
            _, regularization_matrix = self.regularization(self.beta)
            if regularization_matrix.shape != (len(self.beta), len(self.beta)):
                raise ValueError('wrong regularization matrix dimensions: regularization_matrix.shape=%r'
                                 % regularization_matrix.shape)
            fact = cholmod.cholesky(regularization_matrix.tocsc(), beta=1.E-12)
            lower_triangular_matrix = fact.L()
            pull_tilde = np.hstack((pull, lower_triangular_matrix.T.dot(self.beta)))

        self.chi2 += pull_tilde.T.dot(pull_tilde)

        self.detail['model'] = pull.T.dot(pull)
        if self.regularization is not None:
            regularization_triangular_matrix = lower_triangular_matrix.T.dot(self.beta)
            self.detail['reg'] = regularization_triangular_matrix.T.dot(regularization_triangular_matrix)

        if self.pull_function.VarianceModel is not None and \
                len(self.pull_function.VarianceModel.pars.free) != 0:
            variance = self.pull_function.VarianceModel(self.gamma, self.beta)
            self.chi2 += np.log(variance).sum()
            self.detail['var_log_det'] = np.log(variance).sum()

        if derivatives:
            if self.regularization is not None:
                derivative_pull_tilde = scipy.sparse.bmat([[derivative_pull, None], [-lower_triangular_matrix.T, None]])
            else:
                derivative_pull_tilde = derivative_pull
            derivative_pull_tilde = derivative_pull_tilde.tocsc()

            t0 = time.time()
            if self.pull_function.VarianceModel is not None and \
                    len(self.pull_function.VarianceModel.pars.free) != 0:
                w_diag = 1/variance
                w_matrix = scipy.sparse.diags(w_diag)
                matrix_variance_pull = (derivative_variance.tocsc().dot(w_matrix.tocsc()))

                self.hess = self.hessian_nr(matrix_variance_pull=matrix_variance_pull, derivative_pull=derivative_pull,
                                            derivative_pull_tilde=derivative_pull_tilde)
                self.grad = self.grad_nr(res=res, w_diag=w_diag, matrix_variance_pull=matrix_variance_pull,
                                         pull_tilde=pull_tilde,
                                         derivative_pull_tilde=derivative_pull_tilde)

            else:
                derivative_pull_tildecsr = derivative_pull_tilde.tocsr()
                self.hess = 2 * derivative_pull_tildecsr.T.dot(derivative_pull_tildecsr)
                self.grad = -2. * derivative_pull_tildecsr.T.dot(pull_tilde)

            self.hessian_construction = time.time() - t0

    def hessian_nr(self, matrix_variance_pull, derivative_pull, derivative_pull_tilde):
        r"""
        Compute the Hessian of the simultaneous fit of the model parameters
        (beta) and th error snake parameters (gamma):

        .. math::
            H = (H)_{ij} =\left( Tr\left( -V^{-1} J_{V,j} V^{-1} J_{V,i} \right) + 2  J_i^T V^{-1} J_j^T\right)_{ij}

        Parameters
        ----------
        matrix_variance_pull : scipy.sparse.csc_matrix or scipy.sparse.bmat
            Product of the derivative of the error snake wrt to beta and gamma and weight matrix, the variance inverse.
        derivative_pull : array
            Derivative of the pull wrt beta parameters
        derivative_pull_tilde : array
            Concatenation of the derivative of the pull wrt beta
            parameters and the regularization cholesky decomposition term

        Returns
        -------
        Hessian of the model and regularization part :math:`H`
        """
        hessian0 = 2 * derivative_pull_tilde.T.dot(derivative_pull_tilde)

        hessian = coo_matrix(hessian0)
        hessian.resize((self.N_PAR, self.N_PAR))
        hessian_csc = hessian.tocsc()

        ddvv = matrix_variance_pull.tocsc()
        trace_derivative_log_det_variance_hessian = -1 * (ddvv.dot(ddvv.T))
        hessian_log_det = trace_derivative_log_det_variance_hessian
        return hessian_csc + hessian_log_det

    def grad_nr(self, res, w_diag, matrix_variance_pull, pull_tilde, derivative_pull_tilde):
        r"""
        Compute the Gradient of the simultaneous fit of the model parameters
        (beta) and th error snake parameters (gamma):

        .. math::
            \frac{\partial \chi^2_{model}(\rho)}{\partial \rho_i} = Tr\left( V^{-1} J_{V,i} \right) -
            2 J_i^T V^{-1}  R -  R^T  V^{-1}  J_{V,i}  V^{-1}  R

        Parameters
        ----------
        res : array
           Array of the model residuals.
        w_diag :
           Diagonal of the inverse of the variance matrix.
        matrix_variance_pull : scipy.sparse.csc_matrix or scipy.sparse.bmat
           Product of the derivative of the error snake wrt to beta and gamma and weight matrix, the variance inverse.
        pull_tilde : array
           Concatenation of the pulls and the regularization cholesky decomposition term
        derivative_pull_tilde : array
           Concatenation of the derivative of the pull wrt beta
           parameters and the regularization cholesky decomposition term

        Returns
        -------
        Gradient of the model and regularization part :math:`\frac{\partial \chi^2_{model}(\rho)}{\partial \rho_i}`
        """
        grad = -2. * derivative_pull_tilde.T.dot(pull_tilde)
        grad0 = np.concatenate([grad, np.zeros(self.gamma.shape)])
        trace_derivative_log_det_variance_grad = 1 * np.array(matrix_variance_pull.sum(axis=1)).ravel()
        pull_derivation_w_pull = - (matrix_variance_pull.dot((w_diag * res**2)))
        resul = grad0 - trace_derivative_log_det_variance_grad - pull_derivation_w_pull
        return resul

    def color_scatter_evaluation(self, derivatives=False):
        r"""
        Evaluation of the color scatter \& its derivatives.

        .. math::
            \chi^{2}_{CS}(\kappa, \sigma_\kappa) =  \ln{|V_{\kappa}( \sigma_\kappa)|} +
            \kappa^T V^{-1}_{\kappa}( \sigma_\kappa) \kappa

        adding to de gradient :

        .. math::
            \frac{\partial \chi^2_{CS}}{\partial \kappa_i} =  2  V_{\kappa}^{-1} \kappa

        .. math::
            \frac{\partial \chi^2_{CS}}{\partial \sigma_{\kappa,i}} =  Tr\left(V_{\kappa}^{-1}
            \frac{\partial V_{\kappa}}{\partial \sigma_{\kappa,i}} \right)	- \kappa^T V_{\kappa}^{-1}
            \frac{\partial V_{\kappa}}{\partial \sigma_{\kappa,i}} V_{\kappa}^{-1} \kappa

        adding to de hessian :

        .. math::
            \frac{\partial^2 \chi^2_{CS}}{\partial \kappa_j \partial \kappa_i} =  2  V_{\kappa}^{-1}

        .. math::
            \frac{\partial^2 \chi^2_{CS}}{\partial  \sigma_{\kappa,j} \partial  \sigma_{\kappa,i}} =
            -Tr\left( V_{\kappa}^{-1}  \frac{\partial V_{\kappa}}{\partial  \sigma_{\kappa,j}} V_{\kappa}^{-1}
            \frac{\partial V_{\kappa}}{\partial  \sigma_{\kappa,i}}  \right) + 2 \kappa^T V^{-1}_{\kappa}
            \frac{\partial V_{\kappa}}{\partial \sigma_{\kappa,i}} V_{\kappa}^{-1}
            \frac{\partial V_{\kappa}}{\partial \sigma_{\kappa,j}} V_{\kappa}^{-1} \kappa

        Parameters
        ----------
        derivatives : bool
           If gradient and hessian are needed.
        """
        sigma_kappa = self.sigma_kappa
        # print(f'sigma_kappa : {sigma_kappa}')
        # sig = np.polyval(sigma_kappa, self.lambda_c_red)
        if derivatives:
            sig, derivative_kappa_covmatrix = self.color_scatter(self.sigma_kappa, jac=True)  ##
            # vandermonde_matrix = np.vander(self.lambda_c_red, len(sigma_kappa)).T
        else :  ##
            sig = self.color_scatter(self.sigma_kappa)  ##

        kappa = self.pull_function.model.pars['kappa_color'].full
        kappa_covmatrix = sig**2
        inv_kappa_covmatrix = 1/kappa_covmatrix

        coomatrix_inv_kappa_covmatrix = coo_matrix(np.diag(inv_kappa_covmatrix))
        kappa_index_start = self.pull_function.model.pars['kappa_color'].indexof()[0]
        total_parameters_number = int(np.sum([self.hess.shape])/2)

        row = kappa_index_start + coomatrix_inv_kappa_covmatrix.row
        col = kappa_index_start + coomatrix_inv_kappa_covmatrix.col
        extended_coomatrix_inv_kappa_covmatrix = coo_matrix((coomatrix_inv_kappa_covmatrix.data, (row, col)),
                                                            shape=(total_parameters_number, total_parameters_number))

        vc_cs = (inv_kappa_covmatrix.dot(kappa**2)).sum()
        self.chi2 += vc_cs
        self.detail['CS_hold'] = vc_cs

        if self.sigma_kappa_fit:
            log_det_cs = np.log(kappa_covmatrix).sum()
            self.chi2 += log_det_cs
            self.detail['CS_log_det'] = log_det_cs

        if derivatives:
            extended_coomatrix_inv_kappa_covmatrix = extended_coomatrix_inv_kappa_covmatrix.tocsc()
            self.hess += 2 * extended_coomatrix_inv_kappa_covmatrix
            self.grad += 2 * extended_coomatrix_inv_kappa_covmatrix.dot(self.rho)

            if self.sigma_kappa_fit:
                # derivative_kappa_covmatrix = (vandermonde_matrix * sig * 2).T
                trace_derivative_log_det_kappa = 1 * inv_kappa_covmatrix.dot(derivative_kappa_covmatrix)
                kappa_derivative_covmatrix_kappa = -1 * derivative_kappa_covmatrix.T.dot(
                    (inv_kappa_covmatrix * kappa)**2
                )

                grad_kappa = trace_derivative_log_det_kappa + kappa_derivative_covmatrix_kappa.ravel()
                trace_product = inv_kappa_covmatrix * derivative_kappa_covmatrix.T
                double_trace_log_det_kappa = - trace_product.dot(trace_product.T)
                derivative_covmatrix = derivative_kappa_covmatrix.T * inv_kappa_covmatrix * kappa
                double_product_derivative_covmatrix_kappa = 2*(derivative_covmatrix * inv_kappa_covmatrix).dot(
                    derivative_covmatrix.T
                )
                hess_kappa = coo_matrix(double_trace_log_det_kappa + double_product_derivative_covmatrix_kappa)
                hess_coo = self.hess.tocoo()

                hessian_combinaison = scipy.sparse.bmat([[hess_coo, None], [None, hess_kappa]], format='csc')

                self.grad = np.hstack((self.grad, grad_kappa))
                self.hess = hessian_combinaison

    def calibration_gaussian_prior(self, eta_covmatrix, derivatives=False):
        r"""
        Compute calibration propagation component of the total :math:`\chi^2`:

        .. math::
            \chi^2_{calib} = \eta^T V_{\eta}^{-1} \eta

        If derivatives are needed:
        adding to de gradient :

        .. math::
            \frac{d \chi^2_{calib}}{d\eta} = V_{\eta}^{-1} \eta

        adding to de hessian :

        .. math::
           \frac{d^2 \chi^2_{calib}}{d\eta^2} =  V_{\eta}^{-1}

        Parameters
        ----------
        eta_covmatrix : float or array
           Calibration uncertainty matrix.
        derivatives : bool
           If gradient and hessian are needed.
        """
        if type(eta_covmatrix) == float:
            eta_covmatrix = np.diag(np.ones((len(self.pull_function.model.bands))) * eta_covmatrix)
        else:
            eta_covmatrix = eta_covmatrix

        coomatrix_eta_covmatrix = coo_matrix(eta_covmatrix)
        inv_coomatrix_eta_covmatrix = scipy.sparse.linalg.inv(coomatrix_eta_covmatrix.tocsc()).tocoo()
        try:
            eta_index_start = self.pull_function.model.pars['photo_calibration'].indexof()[0]
        except KeyError:
            eta_index_start = self.pull_function.model.pars['eta_calib'].indexof()[0]
        if eta_index_start == -1:
            eta_index_start = 0

        row = eta_index_start + inv_coomatrix_eta_covmatrix.row
        col = eta_index_start + inv_coomatrix_eta_covmatrix.col

        extended_inv_cscmatrix_eta_covmatrix = coo_matrix((inv_coomatrix_eta_covmatrix.data, (row, col)),
                                                          shape=(self.N_PAR, self.N_PAR)).tocsc()
        v_eta = (extended_inv_cscmatrix_eta_covmatrix.dot(self.rho**2)).sum()

        self.chi2 += v_eta
        self.detail['C_eta'] = v_eta

        if derivatives:
            self.hess += 2 * extended_inv_cscmatrix_eta_covmatrix
            self.grad += 2 * extended_inv_cscmatrix_eta_covmatrix @ self.rho

    def get_constrains_derivatives(self, derivatives=False):
        r"""
        Evaluate the constrains :math:`C(\beta)` contribution the the :math:`\chi^2` as a quadratic penalty:

        .. math::
            \chi^2_{cons} = \mu_{pen} C(\beta)^T C(\beta)

        If derivatives are needed:
        adding to de gradient :

        .. math::
            \frac{d \chi^2_{cons}}{d\beta} = 2 \mu_{pen} \frac{\partial C(\beta)}{\partial \beta_i}^T C(\beta)

        adding to de hessian :

        .. math::
            \frac{d^2 \chi^2_{cons}}{d\beta^2} = 2 \mu_{pen} \left(\frac{\partial^2
            C(\beta)}{\partial \beta_j \partial \beta_i}^T C(\beta) +
            \frac{\partial C(\beta)}{\partial \beta_i}^T \frac{\partial C(\beta)}{\partial \beta_j} \right)

        Parameters
        ----------
        derivatives : bool
           If gradient and hessian are needed.
        """
        con = self.constrains(self.beta, jac=False)

        self.chi2 += (con**2).sum()
        self.detail['cons_qua'] = (con**2).sum()
        if len(self.pull_function.model.pars['X1'].free) != 0.:
            if derivatives:
                p_free = self.pull_function.VarianceModel.pars.free
                vcons, jacobian_cons, hessian_cons = self.constrains.var_x1(self.beta,
                                                                            gamma=p_free,
                                                                            jac=True)
                self.hess += hessian_cons.tocsc()
                self.grad += jacobian_cons

            else:
                vcons = self.constrains.var_x1(self.beta, jac=False)
            self.chi2 += vcons**2
            self.detail['x1_cons'] = vcons**2

        if derivatives:
            v, bloc_hessian_cons = self.constrains(self.beta, jac=True)
            if len(self.gamma) != 0.:
                bloc_hessian_cons.resize((bloc_hessian_cons.shape[0], self.N_PAR))
            self.hess += (2 * bloc_hessian_cons.T.dot(bloc_hessian_cons)).tocsc()
            self.grad -= 2 * bloc_hessian_cons.T.dot(v)


class ModelPulls:
    r"""
    Give the pulls of the model.
    For data point i, evaluated the model and the error model : :math:`\sigma` :

    .. math::
        pull = \frac{data_i - model_i(\beta)}{\sigma_i}


    .. note: ModelResiduals() should be able to accept either a model or a variance model !
    .. note: shorter code if model() could have the same signature regardless of jac=True or not

    Attributes
    ----------
    training_dataset : nacl.dataset.TrainingDataset
        Data set of photometric and spectroscopic observations.
    idxlc : int
        Index where light curve data finish and spectra data starts.
    data : array
        Data point array.
    N : int
        Number of data point.
    model : nacl.salt.
        Model
    chi2_normalization : None or float
        Normalization between modelization of photometric and spectroscopic datat
        :math:`\chi^2_{photo}` and :math:`\chi^2_{spectro}`.
    VarianceModel : None or nacl.models.variancemodels
        Variance model, error snake integration.
    pars : FitParameters
        Model parameters.
    """

    def __init__(self, model, variance_model=None, chi2_normalization=None, fit_spec=True):
        r"""
        Model pull initialisation.

        Parameters
        ----------
        model : nacl.models.salt
            Model.
        chi2_normalization : None or float
            Normalization between modelization of photometric and spectroscopic datat
            :math:`\chi^2_{photo}` and :math:`\chi^2_{spectro}`.
        variance_model : None or nacl.models.variancemodels
            Variance model, error snake integration.
        fit_spec : bool
            If spectroscopic data are fitted.
        """
        self.training_dataset = model.training_dataset
        self.idxlc = len(self.training_dataset.lc_data)
        if fit_spec:
            self.flux = np.hstack((self.training_dataset.lc_data.flux,
                                  self.training_dataset.spec_data.flux))
            self.fluxerr = np.hstack((self.training_dataset.lc_data.fluxerr,
                                     self.training_dataset.spec_data.fluxerr))
            # self.data = np.hstack((self.training_dataset.lc_data,
            #                        self.training_dataset.spec_data))
        else:
            self.flux = self.training_dataset.lc_data.flux
            self.fluxerr = self.training_dataset.lc_data.fluxerr
            # self.data = self.training_dataset.lc_data
        self.N = len(self.flux)
        self.model = model
        self.chi2_normalization = chi2_normalization
        # the code line below are rather strange.
        # I think the reason it is written that way is that Guy was working
        # with several parameter vectors. Now, all the parameters have beem
        # grouped into a single vector.
        # TODO: rewrite
        self.VarianceModel = None
        if variance_model is not None:
            self.VarianceModel = variance_model
        else:
            self.pars = model.pars

    def __call__(self, beta, gamma=[], jac=True):
        r"""
        Evaluation of the pull.

        Parameters
        ----------
        beta : array
           Model parameters.
        gamma : array
           Error snake parameters.
        jac : bool
           If derivatives are required.

        Returns
        -------
        w_res : array
            Residuals multiply by the square root of the weight matrix.
        v : array
            Model evaluation.

        if jac is True :
        w_res : array
            Residuals multiply by the square root of the weight matrix.
        w_jac : scipy.sparse.coo_matrix
            Residuals derivatives multiply by the square root of the weight matrix.
        v : array
            Model evaluation.
        jacobian : scipy.sparse.coo_matrix
             Model derivative evaluation.
        variance : array or None
             Error snake evaluation.
        derivative_variance : scipy.sparse.coo_matrix or None
            Error snake derivative evaluation.
        """
        if jac:
            v, jacobian = self.model(beta, jac=True)
        else:
            v = self.model(beta, jac=False)

        # res = self.data['Flux'] - v
        res = self.flux - v

        if len(gamma) != 0:
            variance = self.VarianceModel(gamma, beta)
        else:
            # variance = self.data['FluxErr']**2
            variance = self.fluxerr**2

        ww = 1/np.sqrt(variance)

        if self.chi2_normalization is None:
            chi2_normalization = len(self.training_dataset.lc_data)/len(self.training_dataset.spec_data)
        else:
            chi2_normalization = self.chi2_normalization

        #print(f'chi2_normalization = {chi2_normalization}')
        ww[self.idxlc:] *= np.sqrt(chi2_normalization)

        if len(variance.shape) == 1:
            w = scipy.sparse.dia_matrix((ww, [0]), shape=(self.N, self.N))
        else:
            w = scipy.sparse.csc_matrix(ww)

        w_res = w @ res
        if jac:
            w_jac = w @ jacobian  # -w @ jacobian #moins

            if len(gamma) != 0:
                variance, derivative_variance = self.VarianceModel(gamma, beta, jacobian=jacobian.tocoo())
                return w_res, w_jac, v, jacobian, variance, derivative_variance
            else:
                return w_res, w_jac, v, jacobian, variance, None

        if np.isnan(w@res).sum() > 0.:
            raise ValueError('There are np.nan in w@res')
        if np.isinf(w@res).sum() > 0.:
            raise ValueError('There are np.inf in w@res')
        return w_res, v
