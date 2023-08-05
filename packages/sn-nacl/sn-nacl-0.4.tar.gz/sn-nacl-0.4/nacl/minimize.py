"""
This module is a rewrite of the minimizers.py module.
"""

import logging
import numpy as np
from sksparse import cholmod
import scipy
import scipy.optimize
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s",
                    level=logging.INFO)

try:
    from sparse_dot_mkl import gram_matrix_mkl, dot_product_mkl
except:
    logging.warning('module: `sparse_dot_mkl` not available')
else:
    logging.info('sparse_dot_mkl found. Building hessian should be faster.')

class Minimizer:
    """Find the minimum of a function using a Newton-Raphson method
    """
    def __init__(self, log_likelihood, n_iter=100,
                 dchi2_stop=0.001, log=None):
        """
        """
        self.log_likelihood = log_likelihood
        self.model = self.log_likelihood.model
        self.n_iter = n_iter
        self.dchi2_stop = dchi2_stop
        self.log = log

    def ndof(self):
        return self.model.training_dataset.nb_meas() - len(self.model.pars.free)

    def _brent(self, pars, dpars):
        """attempt to save the day with a line search
        """
        def min_1d_func(t):
            return self.log_likelihood(pars.free + t * dpars.free)

        # ret = pars.copy()
        logging.info('linesearch (brent)...')
        t, val, ni, funcalls = \
            scipy.optimize.brent(min_1d_func, brack=(0., 1.),
                                 full_output=True)
        # ret.free = pars.free + t * dpars.free
        logging.info(f'done: t={t}, val={val}')
        # logging.info(f'{val} == {self.log_likelihood(pars.free)}')
        return t

    def minimize(self, p_init, mode='supernodal', ordering_method='metis',
                 beta=0., linesearch=False, dchi2_stop=None):
        """Minimize the log-likelihood
        """
        pars = self.model.pars
        pars.free = p_init
        dchi2_stop = dchi2_stop if dchi2_stop is not None else self.dchi2_stop
        dpars = self.model.pars.copy()
        old_pars = pars.copy()
        dpars.full[:] = 0.


        # minimization loop
        old_chi2 = None
        for i in range(self.n_iter+1):
            logging.info(f'nacl.minimizer: {i}')
            chi2, grad, hessian = self.log_likelihood(pars.free,
                                                      deriv=True)
            try:
                logging.info('cholesky...')
                fact = cholmod.cholesky(hessian.tocsc(),
                                        mode=mode,
                                        ordering_method=ordering_method,
                                        beta=beta)
                logging.debug('done.')
            except:
                logging.error(f'cholesky failed: matrix non-posdef')
                return {'pars': pars.copy,
                        'chi2': chi2,
                        'ndof': len(pars.free),
                        'status': 'Cholesky failed',
                        'grad': grad,
                        'hessian': hessian}
            dpars.free = fact(grad)

            # print(dpars.free)

            # store previous parameter values
            old_chi2 = chi2
            old_pars.free = pars.free
            pars.free = pars.free + dpars.free
            # and recompute the chi2
            chi2 = self.log_likelihood(pars.free, deriv=False)
            # chi2 decrement
            dchi2 = old_chi2 - chi2

            if dchi2 < 0 & (np.abs(dchi2) > dchi2_stop):
                logging.warning(f'increasing chi2: dchi2={dchi2:.4e}')
                t = self._brent(old_pars, dpars)
                pars.free = old_pars.free + t * dpars.free
                chi2 = self.log_likelihood(pars.free, deriv=False)
                dchi2 = old_chi2 - chi2
                if dchi2 < 0.:
                    logging.warning(f'increasing chi2: {old_chi2} -> {chi2}')
                    # revert to the previous step
                    pars.free = old_pars.free
                    return {'pars': pars.copy(),
                            'chi2': chi2,
                            'ndof': len(pars.free),
                            'status': 'increasing chi2'}

            # maybe we have converged ?
            if np.abs(dchi2) <= dchi2_stop:
                logging.info(f'converged: dchi2={dchi2:.4e}: {old_chi2:12.9g} -> {chi2:12.9g} ndof={self.ndof()} chi2/ndof={chi2/self.ndof()}')
                return {'pars': pars.copy(),
                        'chi2': chi2,
                        'ndof': len(pars.free),
                        'status': 'converged'}

            # and maybe we have exceeded the number of iterations ?
            if i >= self.n_iter:
                logging.info(f'iter {i} dchi2={dchi2:.4e}: {old_chi2:12.9g} -> {chi2:12.9g} ndof={self.ndof()} chi2/ndof={chi2/self.ndof()}')
                return {'pars': pars.copy(),
                        'chi2': chi2,
                        'ndof': len(pars.free),
                        'status': 'too many iterations'}

            logging.info(f'iter {i} dchi2={dchi2:.4e}: {old_chi2:12.9g} -> {chi2:12.9g} ndof={self.ndof()} chi2/ndof={chi2/self.ndof()}')

    def __call__(self, p_init, mode='supernodal', ordering_method='metis',
                 beta=0., linesearch=False):
        """Minimize the log-likelihood
        """
        pars = self.model.pars
        pars.free = p_init
        dpars = self.model.pars.copy()
        pars_before = pars.copy()
        dpars.full[:] = 0.

        # minimization loop
        old_chi2 = None
        for i in range(self.n_iter):
            logging.info(f'nacl.minimizer: {i}')
            chi2, grad, hessian = self.log_likelihood(pars.free,
                                                      deriv=True)
            # maybe we are close to the minimum already ?
            if old_chi2 is not None:
                dchi2 = old_chi2 - chi2
                if (np.abs(dchi2) < self.dchi2_stop):
                    logging.info(f'converged: dchi2={dchi2:.4e}: {old_chi2:12.9g} -> {chi2:12.9g} ndof={self.ndof()} chi2/ndof={chi2/self.ndof()}')
                    return {'pars': pars.copy(),
                            'chi2': chi2,
                            'ndof': len(pars.free),
                            'status': 'converged'}
                if dchi2 < 0.:
                    logging.warning(f'increasing chi2: {old_chi2} -> {chi2}')
                    # revert to the previous step
                    pars.free = pars_before.free
                    return {'pars': pars.copy(),
                            'chi2': chi2,
                            'ndof': len(pars.free),
                            'status': 'increasing chi2'}
                if i >= self.n_iter:
                    return {'pars': pars.copy(),
                            'chi2': chi2,
                            'ndof': len(pars.free),
                            'status': 'too many iterations'}
                logging.info(f'iter {i} dchi2={dchi2:.4e}: {old_chi2:12.9g} -> {chi2:12.9g} ndof={self.ndof()} chi2/ndof={chi2/self.ndof()}')
            # else:
                # logging.info(f'first step - ')
            # if not, let's compute the next Newton-Raphson step...
            try:
                logging.info('cholesky...')
                fact = cholmod.cholesky(hessian.tocsc(),
                                        mode=mode,
                                        ordering_method=ordering_method,
                                        beta=beta)
                logging.info('done.')
            except:
                logging.error(f'cholesky failed: matrix non-posdef')
                return {'pars': pars.copy,
                        'chi2': chi2,
                        'ndof': len(pars.free),
                        'status': 'Cholesky failed',
                        'grad': grad,
                        'hessian': hessian}
            dpars.free = fact(grad)

            if linesearch:

                def min_1d_func(t):
                    return self.log_likelihood(pars_before.free + \
                                               t * dpars.free)

                logging.info('linesearch (brent)...')
                t, val, ni, funcalls = \
                    scipy.optimize.brent(min_1d_func, brack=(0., 1.),
                                         full_output=True)
                pars.free = pars_before.free + t * dpars.free
                logging.info(f'done: t={t}, val={val}')
                logging.info(f'{val} == {self.log_likelihood(pars.free)}')

            else:
                pars.free = pars_before.free + dpars.free

            if old_chi2 and (old_chi2 < chi2):
                # if increasing chi2 detected, then linesearch
                t = self._brent(pars_before, dpars)
                pars.free = pars_before.free + dpars.free

            # and update the old values
            old_chi2 = chi2
            pars_before.free = pars.free


class LogLikelihood2:
    """Compute a LogLikelihood and its derivatives from a model.

    The main purpose of this class, is to assemble the ingredients of the
    linearized normal equations, from (1) a model (2) a dataset (3) optional
    add-ons such as contraints, regularization and an error model.

    It was written to mimimize the typical Likelihood of the NaCl model
    (see Guy's thesis, equation (1) page XX).
    """

    def __init__(self, model, cons=None, reg=None, variance_model=None,
                 force_default_spgemm=False):
        """
        """
        self.model = model
        self.training_dataset = model.training_dataset
        self.pars = self.model.pars.copy()
        self.cons = cons if cons is not None else []
        self.reg = reg if reg is not None else []
        self.variance_model = variance_model
        self.y = self.training_dataset.get_all_fluxes()
        self.yerr = self.training_dataset.get_all_fluxerr()
        self.bads = self.training_dataset.get_valid() == 0
        self.force_default_spgemm = force_default_spgemm

    def __call__(self, p, deriv=False):
        """evaluate for the current parameters
        """
        self.model.pars.free = p

        # the ingredients
        bads = self.bads
        model_flux, model_jac = None, None
        model_var, model_var_jac = 0., None
        chi2, log_det_v = 0., 0.

        # just for logging purposes
        main_chi2 = 0.
        cons_chi2 = []
        reg_chi2 = []

        # if no derivatives requested,
        # just add the penalities and we should be ok
        if not deriv:
            # model and variance
            model_flux = self.model(p, jac=False)
            var = self.yerr**2
            if self.variance_model is not None:
                model_var = self.variance_model(model_flux=model_flux)
                var += model_var
                log_det_v = np.log(var[~bads]).sum()

            # weighted residuals
            res = self.y - model_flux
            sig = np.sqrt(var)
            wres = res / sig

            if hasattr(self, 'debug'):
                self.chi2_debug = (wres[~bads]**2).sum()
                self.log_det_v_debug = log_det_v
                self.full_chi2_debug = self.chi2_debug + log_det_v

            # and the chi2
            chi2 = (wres[~bads]**2).sum() + log_det_v
            for cons in self.cons:
                chi2 += cons(p, deriv=False)
            for reg in self.reg:
                chi2 += reg(p, deriv=False)
            return chi2

        # that was the easy part. Now, when derivatives requested
        # things are little more complicated.
        logging.debug('model (jac=True)')
        model_flux, model_jac = self.model(p, jac=True)
        var = self.yerr**2
        if self.variance_model is not None:
            logging.debug('variance model (jac=True)')
            model_var, model_var_jac = \
                self.variance_model(model_flux=model_flux,
                                    model_jac=model_jac,
                                    jac=True)
            var += model_var
            log_det_v = np.log(var[~bads]).sum()

        # weighted residuals
        res = self.y - model_flux
        w = 1. / np.sqrt(var)
        N = len(self.y)
        W = scipy.sparse.dia_matrix((w, [0]), shape=(N, N))
        w_res = W @ res
        w_J = W @ model_jac

        # cut the bads
        w_J = w_J[~bads,:]
        w_res = w_res[~bads]

        # chi2
        main_chi2 = chi2 = (w_res**2).sum()
        chi2 += log_det_v

        if hasattr(self, 'debug'):
            self.chi2_debug = main_chi2
            self.log_det_v_debug = log_det_v
            self.full_chi2_debug = chi2

        # the gradient and hessian have several components
        # first, the two classical ones: J^TWJ and J^TWR
        grad = 2. * w_J.T @ w_res
        w_J = w_J.tocsr()
        if 'gram_matrix_mkl' in globals() and not self.force_default_spgemm:
            logging.info('hessian: H = J.T @ J (gram_matrix_mkl)')
            # `reorder_output=True` seems essential here.
            # otherwise, the Newton-Raphson step is wrong, typically
            # by a factor 0.5 ... this is scary, I know...
            hess = 2. * gram_matrix_mkl(w_J, reorder_output=True)
            row, col = hess.nonzero()
            hess[col,row] = hess[row,col]
            # hess = 2. * dot_product_mkl(w_J.T, w_J, reorder_output=True)
        else:
            logging.info('hessian: H = J.T @ J (slow version)')
            hess = 2. * w_J.T @ w_J

        # model_jac.data *= w[model_jac.row]
        # main_chi2 = chi2 = (wres[~bads]**2).sum()
        # chi2 += log_det_v
        # wres = wres[~bads]

        # then, the contributions of the (optional) variance model
        # to the hessian and gradient
        # TODO:
        #  - remove outliers from the model jacobian
        #  - if W @ J faster, do that
        if self.variance_model is not None:
            logging.debug('variance model')
            WW = scipy.sparse.dia_matrix((w**2, [0]), shape=(N, N))
            # model_var_jac.data /= var[model_var_jac.row]
            model_var_jac = (WW @ model_var_jac)[~bads, :]

            # gradient
            # was +1
            # rWdVWr = -1. * (w_res**2).sum() * np.array(model_var_jac.T.sum(axis=1)).squeeze()
            mvJ = model_var_jac.tocoo()
            wres_mvJ = scipy.sparse.coo_matrix(
                (mvJ.data * w_res[mvJ.row],
                 (mvJ.row, mvJ.col)),
                 shape=mvJ.shape)
            rWdVWr = 1. * wres_mvJ.T @ w_res

            # rWdVWr = -1. * (w_res**2 * np.array(model_var_jac.T)).sum(axis=1).squeeze()
            grad += rWdVWr
            # was -1
            tr_WdV = -1. * np.array(model_var_jac.T.sum(axis=1)).squeeze()
            grad += tr_WdV

            # hessian
            tr_WdVWdV = 1. * model_var_jac.T.dot(model_var_jac)
            hess += tr_WdVWdV

        # the quadratic constraints
        # logging.info('constraints')
        for penality in self.cons:
            v_pen, grad_pen, hess_pen = penality(p, deriv=True)
            chi2 += v_pen
            grad += grad_pen
            hess += hess_pen
            cons_chi2.append(v_pen)

        # the regularization
        # logging.info('regularization')
        for penality in self.reg:
            v_pen, grad_pen, hess_pen = penality(p, deriv=True)
            chi2 += v_pen
            grad += grad_pen
            hess += hess_pen
            reg_chi2.append(v_pen)

        msg = f'chi2={main_chi2:.6e} | log_det_v={log_det_v} | cons='
        for cons_val in cons_chi2:
            msg += f'{cons_val:.6e}'
        msg += ' | reg='
        for reg_val in reg_chi2:
            msg += f'{reg_val:.6e}'
        logging.info(msg)

        return chi2, grad, hess


class LogLikelihood:
    """Compute a LogLikelihood and its derivatives from a model.

    The main purpose of this class, is to assemble the ingredients of the
    linearized normal equations, from (1) a model (2) a dataset (3) optional
    add-ons such as contraints, regularization and an error model.

    It was written to mimimize the typical Likelihood of the NaCl model
    (see Guy's thesis, equation (1) page XX).
    """

    def __init__(self, wres_func, cons=None, reg=None, error_snake=None):
        """
        """
        self.func = wres_func
        self.model = self.func.model
        self.pars = self.func.model.pars.copy()
        self.cons = cons if cons is not None else []
        self.reg = reg if reg is not None else []
        self.error_snake = error_snake if error_snake is not None else []
        self.bads = wres_func.model.training_dataset.get_valid() == 0

    def __call__(self, p, deriv=False):
        """evaluate for the current parameters
        """
        self.model.pars.free = p
        bads = self.bads

        # if no derivatives requested,
        # just add the penalities and we should be ok
        if not deriv:
            w_res = self.func(p, jac=False)
            chi2 = (w_res[~bads]**2).sum()
            for cons in self.cons:
                chi2 += cons(p, deriv=False)
            for reg in self.reg:
                chi2 += reg(p, deriv=False)
            return chi2

        # if derivatives requested, then
        # 1) base chi2 + gradient + hessian
        w_res, w_J, _ = self.func(p, jac=True)
        w_res = w_res[~bads]
        w_J = w_J[~bads,:]
        chi2 = (w_res**2).sum()
        grad = 2. * w_J.T @ w_res
        hess = 2. * w_J.T @ w_J

        # just for logging purposes
        main_chi2 = chi2
        cons_chi2 = []
        reg_chi2 = []

        # add the penalities and their derivatives
        for penality in self.cons:
            v_pen, grad_pen, hess_pen = penality(p, deriv=True)
            chi2 += v_pen
            grad += grad_pen
            hess += hess_pen
            cons_chi2.append(v_pen)

        for penality in self.reg:
            v_pen, grad_pen, hess_pen = penality(p, deriv=True)
            chi2 += v_pen
            grad += grad_pen
            hess += hess_pen
            reg_chi2.append(v_pen)

        msg = f'chi2={main_chi2:.6e} | cons='
        for cons_val in cons_chi2:
            msg += f'{cons_val:.6e}'
        msg += ' | reg='
        for reg_val in reg_chi2:
            msg += f'{reg_val:.6e}'
        logging.info(msg)

        return chi2, grad, hess


class WeightedResiduals:

    def __init__(self, model, variance_model=None):
        """constructor - iniate the residual function
        """
        self.model = model
        self.training_dataset = model.training_dataset
        self.variance_model = variance_model
        self.y = self.training_dataset.get_all_fluxes()
        self.yerr = self.training_dataset.get_all_fluxerr()

    def __call__(self, p, jac=False):
        """evaluate
        """
        self.model.pars.free = p

        # evaluate the residuals
        val, J = None, None
        if jac:
            val, J = self.model(p, jac=True)
        else:
            val = self.model(p, jac=False)
        res = self.y - val

        # measurement variance and weights
        var, Jvar = 0., None
        if self.variance_model is not None:
            if not jac:
                var = self.variance_model(p, jac=False)
            else:
                var, Jvar = self.variance_model(p, jac=True)

        res_var = self.yerr**2 + var
        w = 1. / np.sqrt(res_var)
        N = len(self.y)
        W = scipy.sparse.dia_matrix((w, [0]), shape=(N, N))

        # weighted residuals
        wres = W @ res
        if jac:
            wJ = W @ J
            return wres, wJ, Jvar
        return wres
